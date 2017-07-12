"""Evaluates the quality of a community"""
from timeit import default_timer as timer
import networkx as nx
import utilities.kmeans_cluster_nodes as kmeans
import utilities.count_edge_cuts as cutcount
import utilities.calculate_modularity as modularity
import utilities.normalised_mutual_information as nmi
import utilities.hamming_cluster_nodes as hamcluster
import utilities.heirarchical_clustering as heircluster

def compute_nmi(comparison_name, partition1, partition2, node_count):
    NMI = nmi.calculate_normalised_mutual_information(partition1, node_count, partition2, node_count)
    print(comparison_name, NMI)

def compute_edge_cut_count(graph, communities):
    COUNT = cutcount.count_edge_cuts(graph, communities)
    print("Edges Cut : ", COUNT)

def compute_modularity(graph, communities):
    MODULARITY = modularity.calculate_modularity(graph, communities)
    print("Modularity : ", MODULARITY)

def print_divider_large():
    print("-----------------------------------------------------")    

def print_divider_sm():
    print("-----------------")

def print_execution_time(end, start):
    print("Time to execute clustering : ", end - start)

def print_cluster_size(size):
    print("Community Count : ", size)

#import the data and generate a graph
DATA_FILE_NAME = 'data/facebook_combined.txt'
#DATA_FILE_NAME = 'data/Wiki-Vote-Sample.txt'
G = nx.read_edgelist(DATA_FILE_NAME, comments='#', create_using=nx.Graph(), nodetype=int)
G.name = DATA_FILE_NAME
heirarchichal_clusters = heircluster.create_hc(G)
print(nx.info(G))

NUMBER_OF_NODES = G.number_of_nodes()
print_divider_sm()
start = timer()
kmeans_clusters = kmeans.cluster_nodes(G, 2)
end = timer()
print("k-means cluster stats")
print_cluster_size(len(kmeans_clusters))
print_execution_time(end, start)
compute_edge_cut_count(G, kmeans_clusters)
compute_modularity(G, kmeans_clusters)
print_divider_sm()

start = timer()
hamming_clusters = hamcluster.create_communities(G, 0.001)
end = timer()
print("hamming distance cluster stats")
print_cluster_size(len(hamming_clusters))
print_execution_time(end, start)
compute_edge_cut_count(G, hamming_clusters)
compute_modularity(G, hamming_clusters)
print_divider_sm()

start = timer()
heirarchichal_clusters = heircluster.create_hc(G)
end = timer()
print("Heirarchichal cluster stats")
print_cluster_size(len(heirarchichal_clusters))
print_execution_time(end, start)
compute_edge_cut_count(G, heirarchichal_clusters)
compute_modularity(G, heirarchichal_clusters)
print_divider_sm()

compute_nmi("NMI kmeans vs hamming : ", kmeans_clusters, hamming_clusters, NUMBER_OF_NODES)
compute_nmi("NMI kmeans vs heirarchichal : ", kmeans_clusters, heirarchichal_clusters, NUMBER_OF_NODES)
compute_nmi("NMI heirarchichal vs hamming : ", hamming_clusters, heirarchichal_clusters, NUMBER_OF_NODES)

print("done")
