from rest_framework.views import APIView
from rest_framework.response import Response
from recommendations.services.faiss_sharded import ShardedFAISS
from recommendations.services.recall import dense_recall, lexical_recall
from recommendations.services.rerank import reranker
from recommendations.models import Video, Segment, Embedding
from recommendations.services.embedding import encode_texts, get_embedder
import numpy as np
# simple in-memory index loader (for dev)
SHARDED_INDEX = None
def load_index():
    global SHARDED_INDEX
    if SHARDED_INDEX is None:
        SHARDED_INDEX = ShardedFAISS(dim=512, shard_paths=[])
    return SHARDED_INDEX
class SearchAPI(APIView):
    def get(self, request):
        q = request.query_params.get('q','').strip()
        if not q: return Response({'error':'empty query'}, status=400)
        user_vec = np.zeros(512,dtype='float32')
        try:
            emb = Embedding.objects.filter(owner_type='video').first()
            if emb:
                user_vec = np.frombuffer(emb.vector, dtype=np.float32)
                user_vec = user_vec / (np.linalg.norm(user_vec)+1e-9)
        except: pass
        idx = load_index()
        dense = idx.search(encode_texts([q])[0], topk=200)
        dense_pks = [pk for pk,_ in dense]
        lex_segs = lexical_recall(q, topn=200)
        lex_video_pks = list({s.video_id for s in lex_segs})
        candidate_pks = list(dict.fromkeys(dense_pks + lex_video_pks))[:500]
        videos = Video.objects.filter(pk__in=candidate_pks)
        candidates=[]
        for v in videos:
            emb = Embedding.objects.filter(owner_type='video', owner_id=v.pk).first()
            if not emb: continue
            vec = np.frombuffer(emb.vector, dtype=np.float32)
            vec = vec / (np.linalg.norm(vec)+1e-9)
            segs = [s for s in lex_segs if s.video_id==v.pk]
            best_seg = segs[0] if segs else None
            best_text = best_seg.transcript if best_seg else ''
            bm25_score = 1.0 if best_seg else 0.0
            score = reranker.score_video(user_vec, q, vec, best_text, bm25_score=bm25_score)
            candidates.append((v.pk, score, vec, best_text, bm25_score))
        selected = reranker.diversify(candidates, k=12)
        out = [{'video_id': v[0], 'score': float(v[1]), 'segment': v[3]} for v in selected]
        return Response({'results': out})
