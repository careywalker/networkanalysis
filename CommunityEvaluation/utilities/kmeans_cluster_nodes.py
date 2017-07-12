"""Cluster graph using kmeans clustering methods"""
from scipy.cluster.vq import vq, kmeans
import numpy as np
import utilities.generate_eigen_positions as eigen
import operator

def cluster_nodes(graph, cluster_count):
    """
    Cluster the graph and returns the set of communities
    """
    NUMBER_OF_NODES = graph.number_of_nodes()

    #Generate eigen positions
    EIGEN_POSITIONS, EIGEN_VECTORS = eigen.generate_eigen_positions(graph, NUMBER_OF_NODES)

    #Generate features
    FEATURES = np.column_stack((EIGEN_VECTORS[:, 1].real, EIGEN_VECTORS[:, 2].real))

    book = kmeans(FEATURES, cluster_count)[0]
    codes = vq(FEATURES, book)[0]

    communities = []
    nodes = np.array(range(graph.number_of_nodes()))

    for i in range(cluster_count):
        communities.append(nodes[codes == i].tolist())

    communities.sort(key=operator.itemgetter(0))

    return communities
                              