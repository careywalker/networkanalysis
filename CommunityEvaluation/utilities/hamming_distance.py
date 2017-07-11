""" This will compute the Hamming Distance for nodes of the graph"""

import numpy as np

def compute_hamming_distance(edge_list1, edge_list2):
    """
    edge_list1: a list of edges for a node
    edge_list2: a list of edges for a node

    parameters are expected to be in the following format:
    [edge1, edge2, edge3, etc...]

    """

    similar_edge_count = len(np.intersect1d(edge_list1[1], edge_list2[1]))

    return similar_edge_count / (len(edge_list1[1]) + len(edge_list2[1]))
