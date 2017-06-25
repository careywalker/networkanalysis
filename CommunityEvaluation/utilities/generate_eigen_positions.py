"""Generates the eigen positions for an adjency matrix"""
import scipy as sp
import networkx as nx

def generate_eigen_positions(graph, number_of_nodes):
    """
    Given an undirected graph, returns an
    array of eigen positions

    Uses networkx.normalized_laplacian_matrix method to generate laplacian matrix
    """

    eigen_positions = dict()
    normalised_laplacian = nx.normalized_laplacian_matrix(graph)
    eigenvalues, eigenvectors = sp.sparse.linalg.eigs(normalised_laplacian, 3, None, 100.0, 'SM')
    eigenvectors = eigenvectors.real

    for i in range(number_of_nodes):
        eigen_positions[i] = eigenvectors[i, 1].real, eigenvectors[i, 2].real

    return eigen_positions, eigenvectors
