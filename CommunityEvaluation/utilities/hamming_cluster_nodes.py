"""
This will take a Graph and return communities
created using the Hamming distance
"""

import utilities.hamming_distance as ham
import numpy as np

def create_communities(graph, distance_coefficient):
    node_edge_list = []
    communities = []
    for node in graph.nodes():
        node_edge_list.append([node, graph.neighbors(node)])

    #print(node_edge_list)
    cluster1 = []
    cluster2 = []
    hamming_distance_results = []
    node_edge_list_length = len(node_edge_list) - 1
    for node in graph.nodes():
        for index, item in enumerate(node_edge_list):
            if node == item[0]:
                node1 = node_edge_list[index]
                for index2, item2 in enumerate(node_edge_list):
                    if index + index2 == node_edge_list_length:
                        break

                    node2 = node_edge_list[index + index2 + 1]
                    result = ham.compute_hamming_distance(node1, node2)
                    hamming_distance_results.append([node1[0], node2[0], result])
                    if result > distance_coefficient:
                        cluster1.append(node2[0])
                    else:
                        cluster2.append(node2[0])
            else:
                continue


    cluster1_final = np.unique([x for x in cluster1 if x not in cluster2])
    cluster2_final = np.unique([y for y in cluster2 if y not in cluster1_final])
    communities.append(np.array(cluster1_final.tolist()))
    communities.append(np.array(cluster2_final.tolist()))
    return communities
