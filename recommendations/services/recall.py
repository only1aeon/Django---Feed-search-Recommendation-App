from .embedding import get_embedder, encode_texts
from .asr_lattice import expected_token_count
from .faiss_sharded import ShardedFAISS
from recommendations.models import Segment, Embedding, Video
import numpy as np
K1=1.2; B=0.75; AVG_LEN=8.0
def bm25_expected(query_tokens, segment):
    score=0.0; seg_len=max(1,len((segment.transcript or '').split()))
    for w in query_tokens:
        f = expected_token_count(w, segment)
        num = f*(K1+1); den = f + K1*(1-B + B*(seg_len/AVG_LEN))
        score += (num/(den+1e-9))
    return score
def lexical_recall(query, topn=200):
    tokens = query.strip().split()
    segs = Segment.objects.all()[:50000]
    scored=[]
    for s in segs:
        sc = bm25_expected(tokens, s)
        if sc>0: scored.append((s,sc))
    scored.sort(key=lambda x:-x[1])
    return [s for s,_ in scored[:topn]]
def dense_recall(query, sharded_index, topn=200):
    qvec = encode_texts([query])[0]
    return sharded_index.search(qvec, topk=topn)
