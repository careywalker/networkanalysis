"""Cluster graph using kmeans clustering methods"""
import networkx as nx
import matplotlib.pyplot as plt
from scipy.cluster.vq import vq, kmeans
import numpy as np

def cluster_nodes(graph, feat, pos, eigen_pos, number_of_communities, node_colors):
    """
    Cluster the graph and generate diagrams

    returns the set of communities
    """
    book = kmeans(feat, number_of_communities)[0]
    codes = vq(feat, book)[0]

    communities = []
    nodes = np.array(range(graph.number_of_nodes()))

    for i in range(number_of_communities):
        communities.append(nodes[codes == i].tolist())

    plt.figure(1)
    for i in range(number_of_communities):
        nx.draw_networkx_nodes(graph,
                               eigen_pos,
                               node_size=40,
                               hold=True,
                               nodelist=communities[i],
                               node_color=node_colors[i]
                              )

    plt.figure(2)
    for i in range(number_of_communities):
        nx.draw_networkx_nodes(graph,
                               pos,
                               node_size=40,
                               hold=True,
                               nodelist=communities[i],
                               node_color=node_colors[i]
                              )

    return communities
                              