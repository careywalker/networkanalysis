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




______________________________________________________________________________________
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
