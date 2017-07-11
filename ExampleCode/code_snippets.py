for node in G.nodes():
    for index, item in enumerate(node_edge_list):
        if node == item[0]:
            node1 = node_edge_list[index]
            for index2, item2 in enumerate(node_edge_list):
                if index + index2 == node_edge_list_length:
                    break

                node2 = node_edge_list[index + index2 + 1]
                result = ham.compute_hamming_distance(node1, node2)
                hamming_distance_results.append([node1[0], node2[0], result])
        else:
            continue


for result in hamming_distance_results:
    if result[2] > 0.25:
        cluster1.append(result[0])
        cluster1.append(result[1])

    if result[2] < 0.25:
        cluster2.append(result[0])
        cluster2.append(result[1])


#cluster graph using Hamming Distance
node_edge_list = []
for node in G.nodes():
    node_edge_list.append([node, G.neighbors(node)])

print(node_edge_list)

cluster1 = []
cluster2 = []
hamming_distance_results = []
node_edge_list_length = len(node_edge_list) - 1
all_edges = G.nodes()
for node_edge in node_edge_list:
    edges = node_edge[1]
    hamming_result = ham.compute_hamming_distance(edges, all_edges)
    print("hamming_result : ", hamming_result)
    if hamming_result > 0.30:
        cluster1.append(node_edge[0])
    else:
        cluster2.append(node_edge[0])

print("cluster1 : ", cluster1)
print("cluster2 : ", cluster2)

print(np.unique(cluster1))
print(np.unique(cluster2))        