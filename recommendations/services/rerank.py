import numpy as np
from .embedding import get_cross_encoder, encode_texts
cross = None
def get_cross():
    global cross
    if cross is None:
        cross = get_cross_encoder()
    return cross
class Reranker:
    def __init__(self):
        self.cross = get_cross()
    def segment_score(self, query, segment_text):
        if not segment_text: return 0.0
        return float(self.cross.predict([(query, segment_text)])[0])
    def score_video(self, user_vec, query, video_vec, best_segment_text, bm25_score=0.0, weights=None):
        if weights is None: weights=dict(alpha=1.0,beta=1.0,delta=1.0,gamma=1.0,exact_boost=3.0)
        cross_s = self.segment_score(query, best_segment_text) if best_segment_text else 0.0
        personal = float(np.dot(user_vec, video_vec))
        sim = float(np.dot(encode_texts([query])[0], video_vec))
        exact = 1.0 if bm25_score>0 else 0.0
        score = weights['alpha']*cross_s + weights['beta']*personal + weights['delta']*sim + weights['gamma']*bm25_score + weights['exact_boost']*exact
        return score
    def diversify(self, candidates, k=12, diversity_penalty=0.7):
        selected=[]
        while len(selected)<k and candidates:
            def penalized(item):
                _, base, vec, *_ = item
                penalty=0.0
                for s in selected:
                    penalty = max(penalty, float(np.dot(s[2], vec)))
                return base - diversity_penalty*penalty
            candidates.sort(key=penalized, reverse=True)
            selected.append(candidates.pop(0))
        return selected
reranker = Reranker()
