"""
https://networkx.github.io/documentation/networkx-1.9/examples/algorithms/blockmodel.html
"""

from collections import defaultdict
import networkx as nx
import numpy
from scipy.cluster import hierarchy
from scipy.spatial import distance
import matplotlib.pyplot as plt


def create_hc(G):
    """Creates hierarchical cluster of graph G from distance matrix"""
    # Extract largest connected component into graph H
    H = list(nx.connected_component_subgraphs(G))[0]
    # Makes life easier to have consecutively labeled integer nodes
    H = nx.convert_node_labels_to_integers(H)

    path_length = nx.all_pairs_shortest_path_length(H)
    distances = numpy.zeros((len(H), len(H)))
    for u,p in path_length.items():
        for v,d in p.items():
            distances[u][v]=d
    # Create hierarchical cluster
    Y = distance.squareform(distances)
    Z = hierarchy.complete(Y)  # Creates HC using farthest point linkage
    # This partition selection is arbitrary, for illustrive purposes
    membership = list(hierarchy.fcluster(Z, t=1.15))
    # Create collection of lists for blockmodel
    partition = defaultdict(list)
    for n, p in zip(list(range(len(H))), membership):
        partition[p].append(n)
    return list(partition.values())

