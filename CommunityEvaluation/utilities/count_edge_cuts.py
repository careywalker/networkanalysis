"""This will count the number of edges before a cut and after a cut"""
import networkx as nx

def count_edge_cuts(graph, communities):
    """
    Will return a count of the difference between the edges in the
    graph and the edges in the communities
    """

    community_edge_count = 0

    for community in communities:
        community_edge_count += len(nx.edges(nx.subgraph(graph, community)))

    return nx.number_of_edges(graph) - community_edge_count
