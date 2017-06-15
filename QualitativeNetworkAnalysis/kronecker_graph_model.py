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

VALUE1 = round(random.random(),1)
VALUE2 = round(random.random(),1)
VALUE3 = round(random.random(),1)
VALUE4 = round(random.random(),1)

INITIATOR_GRAPH = [[VALUE1, VALUE2], [VALUE3, VALUE4]]
POWER = 3
DECIMAL_PLACES = 3

KRONECKER_MATRIX = Kron.compute_kronecker_product(INITIATOR_GRAPH, POWER, DECIMAL_PLACES)

print("Length of matrix: ", len(KRONECKER_MATRIX))

# for elem in INITIATOR_GRAPH:
#     print(elem)

# for elem in KRONECKER_MATRIX:
#     print(elem)

#convert KRONECKER_MATRIX into a numpy matrix which can then be used
#as the data source for a graph
A = np.matrix(KRONECKER_MATRIX)
#create graph from numpy matrix
G = nx.from_numpy_matrix(A)
NUMBER_OF_NODES = nx.number_of_nodes(G)
DEGREE_THRESHOLD = 1
DEGREE_SEQUENCE = sorted(nx.degree(G, nbunch=None, weight=None).values(), reverse=True)
A = sorted([degree for degree in np.asarray(DEGREE_SEQUENCE) if degree >= DEGREE_THRESHOLD], reverse=True)

# and draw a histogram of the degree distribution
pylab.hist(A, 50)
pylab.grid(True)
pylab.xlabel("Node Degree")
pylab.ylabel("Number of Nodes")
pylab.title("Kronecker Model Synthetic Network | Node Count: " + str(NUMBER_OF_NODES))
pylab.show()

# plot the log-log values
DEGREE_LOG_VALUES = []
RANK_LOG_VALUES = []
for f in A:
    RANK_LOG_VALUES.append(math.log(A.index(f)+1/NUMBER_OF_NODES))
    DEGREE_LOG_VALUES.append(math.log(f))

SLOPE, INTERCEPT, R_VALUE, P_VALUE, SLOPE_STD_ERROR = stats.linregress(DEGREE_LOG_VALUES, RANK_LOG_VALUES)

print("Slope ", SLOPE)
print("Y-intercept ", INTERCEPT)
print("Alpha ", CommFunc.calculatealpha(SLOPE))

X = np.array(DEGREE_LOG_VALUES)
Y = np.array(RANK_LOG_VALUES)
# Calculate some additional outputs
PREDICT_Y = INTERCEPT + SLOPE * X
PRED_ERROR = Y - PREDICT_Y
DEGREES_OF_FREEDOM = len(X) - 2
RESIDUAL_STD_ERROR = np.sqrt(np.sum(PRED_ERROR**2) / DEGREES_OF_FREEDOM)

# Plotting
pyl.plot(X, Y, 'o')
pyl.plot(X, PREDICT_Y, 'k-')
pyl.grid(True)
plt.title("Kronecker Model Synthetic Network Degree Distribution | Node Count: " + str(NUMBER_OF_NODES))
plt.ylabel("Log Rank")
plt.xlabel("Log Degree")
pyl.show()

print("done")
