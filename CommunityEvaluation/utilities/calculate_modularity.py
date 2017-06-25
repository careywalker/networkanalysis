"""This uses Newman-Girwan method for calculating modularity"""
import math
import networkx as nx

def calculate_modularity(graph, communities):
    """
    Loops through each community in the graph
    and calculate the modularity using Newman-Girwan method

    modularity: identify the set of nodes that intersect with each
    other more frequently than expected by random chance
    """

    modularity = 0
    sum_of_degrees_in_community = 0
    number_of_edges_in_community = 0
    number_of_edges_in_network = nx.number_of_edges(graph)

    for community in communities:
        number_of_edges_in_community = len(nx.edges(nx.subgraph(graph, community)))
        for key, value in nx.subgraph(graph, community).degree().items():
            sum_of_degrees_in_community += value
        
        community_modularity = (
            number_of_edges_in_community / number_of_edges_in_network
            ) - math.pow((sum_of_degrees_in_community/(2*number_of_edges_in_network)), 2)

        modularity += community_modularity
        sum_of_degrees_in_community = 0

    return modularity
