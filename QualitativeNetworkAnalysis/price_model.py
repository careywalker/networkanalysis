"""This generates a synthetic network using Price's Model"""
import math
import random
import pylab as pyl    # only if you want graphics
import utilities.average_accumulator as AvgAcc
import numpy as np
from scipy import stats
import networkx as nx
import matplotlib.pyplot as plt

def calculatealpha(slope):
    """Calculate the alpha value given a slope"""
    return abs(slope) + 1

DNETWORK = {}       # dictionary of lists
INODES = 10000      # total number of nodes
NODERANGE = range(INODES)
NODETOATTACHTO = []
COUNTER = 0
DEGREE_THRESHOLD = 1
GRAPH_TYPE = "Price Model Synthetic Network"

AVERAGEACCUMULATOR = AvgAcc.AverageAccumulator()
AVERAGEACCUMULATOR.accumulateValues(0, INODES)

for i in NODERANGE:
    DNETWORK[i] = [] # initialize node of key i with empty list

for node in DNETWORK.values():
    averagedegrees = AVERAGEACCUMULATOR.calculateAverage()
    phi = averagedegrees/(averagedegrees + 1)
    r = random.random() #random.random returns a random number between 0 and 1
    if r > phi:
        j = random.randint(0, len(DNETWORK) - 1)
        DNETWORK[j].append(COUNTER)
        AVERAGEACCUMULATOR.accumulateValues(1, 0)

    if r <= phi:
        AVERAGEOUTDEGREE = 1
        TOTALNODECOUNT = len(DNETWORK)
        INTERVALVALUE = round(r * (TOTALNODECOUNT * AVERAGEOUTDEGREE))
        for destinationnode in DNETWORK.values():
            INDEGREECOUNT = len(node)
            if INDEGREECOUNT >= INTERVALVALUE:
                if len(NODETOATTACHTO) == 0:
                    NODETOATTACHTO = destinationnode
                if INDEGREECOUNT <= len(NODETOATTACHTO):
                    NODETOATTACHTO = destinationnode

        NODETOATTACHTO.append(COUNTER)
        AVERAGEACCUMULATOR.accumulateValues(1, 0)
        NODETOATTACHTO = []

    COUNTER += 1

print("Total Degrees: ", AVERAGEACCUMULATOR.valueAccumulator)
print("Total Nodes: ", AVERAGEACCUMULATOR.countAccumulator)
print("Average Degrees: ", AVERAGEACCUMULATOR.calculateAverage())
# calculate the degree distribution
LDEGREES = sorted([len(node) for node in DNETWORK.values() if len(node) >= DEGREE_THRESHOLD], reverse=True)
#print(LDEGREES)

# and draw a histogram
pyl.hist(LDEGREES, 50)
pyl.xlabel("Node Degree")
pyl.ylabel("Number of Nodes")
pyl.title(GRAPH_TYPE + " | Node Count: " + str(INODES))
pyl.show()

A = LDEGREES
G = nx.DiGraph(DNETWORK)
DEGREE_LOG_VALUES = []
RANK_LOG_VALUES = []
for f in A:
    RANK_LOG_VALUES.append(math.log(A.index(f)+1/INODES))
    DEGREE_LOG_VALUES.append(math.log(f))

SLOPE, INTERCEPT, R_VALUE, P_VALUE, SLOPE_STD_ERROR = stats.linregress(DEGREE_LOG_VALUES, RANK_LOG_VALUES)
ASSORTATIVITY_COEFFICIENT = nx.degree_assortativity_coefficient(G)
CLUSTERING_COEFFICIENT = nx.average_clustering(G.to_undirected())

print("Slope ", SLOPE)
print("Y-intercept ", INTERCEPT)
print("Alpha ", calculatealpha(SLOPE))
print("Assortavity Coefficient: {0:0.2f}".format(ASSORTATIVITY_COEFFICIENT))
print("Average Clustering: {0:0.2f}".format(CLUSTERING_COEFFICIENT))

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
plt.title(GRAPH_TYPE + " |  Degree Distribution | Node Count: " + str(INODES))
plt.ylabel("Log Rank")
plt.xlabel("Log Degree")
pyl.show()
