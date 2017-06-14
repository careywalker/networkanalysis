"""This uses the Kronecker Graph for network analysis"""
import math, random
import pylab     # only if you want graphics
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab as pyl
from scipy import stats
import utilities.common_functions as CommFunc
import utilities.kronecker_product as Kron
import utilities.average_accumulator as AvgAcc

INITIATOR_GRAPH = [[0, 1], [2, 3]]
POWER = 3

KRONECKER_MATRIX = Kron.compute_kronecker_product(INITIATOR_GRAPH, POWER)

print("Length of matrix: ", len(KRONECKER_MATRIX))
