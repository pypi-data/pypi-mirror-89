import numpy as np
from forestknn.utils import *

def matching_leaf_indexes(x, leaf_idx):
    return (x == leaf_idx).astype(int)

def get_matching_leaf_indexes(xs, leaf_idxs):
    matches = list(map(lambda x: matching_leaf_indexes(*x), zip(xs.T, leaf_idxs.T)))
    return np.vstack(matches)

def calculate_neighbor_weights(match_idxs):
    return match_idxs.sum(axis=0)/match_idxs.sum()

def neighbor_weights(estimator, neighborhood, query):
    neighborhood_leaf_idxs = estimator.apply(neighborhood)
    query_leaf_idx = estimator.apply(query)
    matches = get_matching_leaf_indexes(neighborhood_leaf_idxs, query_leaf_idx)
    wts = calculate_neighbor_weights(matches)
    return wts

def adaptive_k_nearest_neighbors(estimator, neighborhood, query, k = 10):
    neighbor_wts = neighbor_weights(estimator, neighborhood, query)
    top_k = get_top_k(neighbor_wts, k)
    knns = neighborhood.iloc[top_k.index].assign(wts = lambda x: top_k.values)
    return knns