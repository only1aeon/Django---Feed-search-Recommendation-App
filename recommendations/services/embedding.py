import numpy as np
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
_EMB_MODEL = None
_CROSS = None
def get_device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'
def get_embedder():
    global _EMB_MODEL
    if _EMB_MODEL is None:
        _EMB_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=get_device())
    return _EMB_MODEL
def get_cross_encoder():
    global _CROSS
    if _CROSS is None:
        _CROSS = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', device=get_device())
    return _CROSS
def encode_texts(texts):
    m = get_embedder()
    embs = m.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    norms = np.linalg.norm(embs, axis=1, keepdims=True) + 1e-9
    return (embs / norms).astype('float32')
