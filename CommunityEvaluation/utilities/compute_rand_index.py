""" This will compute the rand index of the communities"""
import networkx as nx

def compute_rand_index(graph, communityone, communitytwo):
    """
    graph: the full graph
    communityone: the community to use in comparison
    communitytwo: the community to use in comparison
    """

    rand_index = 0
    community_one_nodes = nx.nodes(nx.subgraph(graph, communityone))
    community_two_nodes = nx.nodes(nx.subgraph(graph, communitytwo))

    for c_one_node in community_one_nodes:
        for c_two_node in community_two_nodes:
            print("c_one_node : ", c_one_node)
            print("c_two_node : ", c_two_node)

    return rand_index
