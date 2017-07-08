"""
This will calculate the Normalised Mutual Information of
two graph partitions

Steps:

1. Take partition one and form a k x k matrix that denotes
if a node is in one of the k clusters
2. Take partition two and form a k x k matrix that denotes
if a node is in one of the k clusters
"""
import math
import networkx as nx
import numpy as np

def calculate_entropy(matrix):
    cummulative_log_value = 0
    for item in matrix:
        if item > 0:
            log_value = (math.log(item, 2) * item)
            cummulative_log_value += log_value

    return -(cummulative_log_value)

def calculate_normalised_mutual_information(x_clusters, x_clusters_node_count, y_clusters, y_clusters_node_count):
    """
    x_clusters: clusters of a graph
    y_clusters: clusters of a graph
    """

    x_clusters_length = len(x_clusters)
    y_clusters_length = len(y_clusters)
    x_matrix = np.zeros((x_clusters_node_count, x_clusters_length), dtype=np.float)
    y_matrix = np.zeros((y_clusters_node_count, y_clusters_length), dtype=np.float)

    cluster_counter = 0
    row_counter = 0
    for cluster in x_clusters:
        for node in cluster:
            x_matrix[row_counter, cluster_counter] = 1
            row_counter += 1

        cluster_counter += 1

    cluster_counter = 0
    row_counter = 0
    for cluster in y_clusters:
        for node in cluster:
            y_matrix[row_counter, cluster_counter] = 1
            row_counter += 1

        cluster_counter += 1

    #print("x_matrix\n", x_matrix)
    #print("y_matrix\n", y_matrix)

    #transpose the x_matrix so that it can be multiplied by y
    t_x_matrix = np.transpose(x_matrix)
    #print("transposed x_matrix\n", t_x_matrix)

    tx_y_matrix = np.matmul(t_x_matrix, y_matrix)
    #print("product of tx_y_matrix * y_matrix\n", tx_y_matrix)

    for x in range(0, tx_y_matrix.shape[0]):
        for y in range(0, tx_y_matrix.shape[1]):
            tx_y_matrix[x, y] = tx_y_matrix[x, y] / x_clusters_node_count

    print("p(x,y) \n", tx_y_matrix)
    print("p(x) = ", np.mean(x_matrix, axis=0))
    print("p(y) = ", np.mean(y_matrix, axis=0))

    h_x = calculate_entropy(np.mean(x_matrix, axis=0))
    h_y = calculate_entropy(np.mean(y_matrix, axis=0))
    h_x_y = calculate_entropy(tx_y_matrix.flatten())

    print("H(x) = ", h_x)
    print("H(y) = ", h_y)
    print("H(x,y) = ", h_x_y)

    i_x_y = h_x + h_y - h_x_y

    print("I(x,y) = ", i_x_y)

    average_marginal_entropy = (h_x + h_y) / 2

    print("average marginal entropy = ", average_marginal_entropy)

    nmi = i_x_y / average_marginal_entropy

    #print("NMI = ", nmi)

    return nmi

#The below is just testing data
#PARTITION1 = [[1, 2, 3, 4], [5, 6, 7, 8]]
#PARTITION2 = [[1, 2, 4], [3, 6], [6, 7, 8]]
#calculate_normalised_mutual_information(PARTITION1, 8, PARTITION2, 8)
