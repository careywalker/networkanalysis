#https://networkx.github.io/documentation/networkx-1.9/examples/drawing/degree_histogram.html
#http://central.scipy.org/item/16/2/basic-linear-regression
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab as pyl
from scipy import stats

def calculatealpha(slope):
    """given the slope calculate the alpha"""
    return abs(slope) + 1

DATA_FILE_NAME = 'data/Wiki-Vote.txt'
DEGREE_THRESHOLD = 100

G = nx.read_edgelist(DATA_FILE_NAME, comments='#', create_using=nx.DiGraph(), nodetype=int)
NUMBER_OF_NODES = nx.number_of_nodes(G)

DEGREE_SEQUENCE = sorted(nx.degree(G, nbunch=None, weight=None).values(), reverse=True)
A = sorted(
    [degree for degree in np.asarray(DEGREE_SEQUENCE) if degree >= DEGREE_THRESHOLD], reverse=True
    )

DEGREE_LOG_VALUES = []
RANK_LOG_VALUES = []
for f in A:
    RANK_LOG_VALUES.append(math.log(A.index(f)+1/NUMBER_OF_NODES))
    DEGREE_LOG_VALUES.append(math.log(f))

SLOPE, INTERCEPT, R_VALUE, P_VALUE, SLOPE_STD_ERROR = stats.linregress(
    DEGREE_LOG_VALUES, RANK_LOG_VALUES
    )
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
plt.title(DATA_FILE_NAME + " Degree Distribution")
plt.ylabel("Log Rank")
plt.xlabel("Log Degree")
pyl.show()
