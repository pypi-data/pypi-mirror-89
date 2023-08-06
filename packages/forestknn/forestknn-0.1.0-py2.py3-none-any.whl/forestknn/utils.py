import numpy as np
from collections import namedtuple

def get_top_k_indexes(x: np.ndarray, k: int) -> np.ndarray:
    topk = np.argpartition(x, -k)[-k:]
    return topk


TopK = namedtuple("TopK", ["values", "index"])

def get_top_k(x: np.ndarray, k:int) -> TopK:
    idxs = get_top_k_indexes(x, k)
    topk = x[idxs]
    sorted_topk_idxs = np.argsort(-topk)
    return TopK(topk[sorted_topk_idxs], idxs[sorted_topk_idxs])