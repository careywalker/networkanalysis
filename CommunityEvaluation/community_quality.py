"""Evaluates the quality of a community"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score
import utilities.generate_eigen_positions as eigen
import utilities.kmeans_cluster_nodes as kmeans
import utilities.count_edge_cuts as cutcount
import utilities.calculate_modularity as modularity
import utilities.compute_rand_index as randindex

#import the data and generate a graph
#DATA_FILE_NAME = 'data/facebook_combined.txt'
DATA_FILE_NAME = 'data/Wiki-Vote-Sample.txt'
G = nx.read_edgelist(DATA_FILE_NAME, comments='#', create_using=nx.Graph(), nodetype=int)
G.name = DATA_FILE_NAME
NUMBER_OF_NODES = G.number_of_nodes()

#1.) Create communities using k-means clustering
#1.1) Generate eigen positions
EIGEN_POSITIONS, EIGEN_VECTORS = eigen.generate_eigen_positions(G, NUMBER_OF_NODES)

#1.2) Generate features
FEATURES = np.column_stack((EIGEN_VECTORS[:, 1].real, EIGEN_VECTORS[:, 2].real))


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
NODE_COLORS = ['red', 'yellow', 'olive', 'aqua', 'blue', 'fuchsia', 'black', 'green']

print(nx.info(G))
print("_____________________________")


for count in range(2, 3):
    COMMUNITIES = kmeans.cluster_nodes(G, FEATURES, POSITIONS, EIGEN_POSITIONS, count, NODE_COLORS)
    #randindex.compute_rand_index(G, COMMUNITIES[0], COMMUNITIES[1])
    X = [1, 0, 0, 1]
    Y = [1, 0, 0, 1, 0, 1]
    NMI = normalized_mutual_info_score(X, Y) #returns 0.345592029944
    #NMI = normalized_mutual_info_score([0, 3, 3, 4], [0, 3, 0, 3]) #returns 0.408248290464
    print("NMI = ", NMI)
    #TODO: Try to see if you can generate a scree plot to
    # #get your K for k-means clustering
    #It should match the largest modularity value, I think it should anyway
    #the k should be the point where the intra cluster distance average has the
    #most significant decrease in change
    print("Community count : ", count)
    print("Number of edges cut in partitioning : ", cutcount.count_edge_cuts(G, COMMUNITIES))
    print("Modularity of the partitioning : ", modularity.calculate_modularity(G, COMMUNITIES))
    print("_____________________________")

#plot_graph(G, EIGEN_POSITIONS, 1)



#plt.show()
print("done")
