"""Evaluates the quality of a community"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import utilities.generate_eigen_positions as eigen
import utilities.kmeans_cluster_nodes as kmeans
import utilities.count_edge_cuts as cutcount
import utilities.calculate_modularity as modularity

#import the data and generate a graph
DATA_FILE_NAME = 'data/facebook_combined.txt'
G = nx.read_edgelist(DATA_FILE_NAME, comments='#', create_using=nx.Graph(), nodetype=int)
NUMBER_OF_NODES = G.number_of_nodes()

#1.) Create communities using k-means clustering
#1.1) Generate eigen positions
EIGEN_POSITIONS, EIGEN_VECTORS = eigen.generate_eigen_positions(G, NUMBER_OF_NODES)

#1.2) Generate features
FEATURES = np.column_stack((EIGEN_VECTORS[:, 1].real, EIGEN_VECTORS[:, 2].real))

#compute modularity

#get the edge cut count

#helper function for plotting the graph
def plot_graph(graph, positions, figure_number):
    """plots the graph of the data"""
    label = dict()
    labelpos = dict()
    for i in range(graph.number_of_nodes()):
        label[i] = i
        labelpos[i] = positions[i][0]+0.02, positions[i][1]+0.02

    fig = plt.figure(figure_number, figsize=(8, 8))

    fig.suptitle(
        "Figure Number : " + str(figure_number),
        fontsize=14, fontweight='bold'
        )

    fig.clf()

    nx.draw_networkx_nodes(graph,
                           positions,
                           node_size=40,
                           hold=False,
                          )

    nx.draw_networkx_edges(graph,
                           positions,
                           hold=True
                          )

    nx.draw_networkx_labels(graph,
                            labelpos,
                            label,
                            font_size=10,
                            hold=True,
                           )


POSITIONS = nx.spring_layout(G)
NODE_COLORS = ['red', 'yellow', 'olive', 'aqua', 'blue', 'fuchsia']

print(nx.info(G))
print("_____________________________")


for count in range(2, 7):
    COMMUNITIES = kmeans.cluster_nodes(G, FEATURES, POSITIONS, EIGEN_POSITIONS, count, NODE_COLORS)
    print("Community count : ", count)
    print("Number of edges cut in partitioning : ", cutcount.count_edge_cuts(G, COMMUNITIES))
    print("Modularity of the partitioning : ", modularity.calculate_modularity(G, COMMUNITIES))
    print("_____________________________")

#plot_graph(G, EIGEN_POSITIONS, 1)



#plt.show()
print("done")
