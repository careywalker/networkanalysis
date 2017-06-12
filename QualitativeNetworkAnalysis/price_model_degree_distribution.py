import math, random
import pylab     # only if you want graphics
import utilities.average_accumulator as AvgAcc
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab as pyl
from scipy import stats

def calculatealpha(slope):
    return abs(slope) + 1

DNETWORK = {}       # dictionary of lists
INODES = 10000       # total number of nodes
NODERANGE = range(INODES)
NODETOATTACHTO = []

AVERAGEACCUMULATOR = AvgAcc.AverageAccumulator()
#AVERAGEACCUMULATOR.accumulateValues(0, INODES)

for i in NODERANGE:
	DNETWORK[i] = []      # initialize node of key i with empty list
	averagedegrees = AVERAGEACCUMULATOR.calculateAverage()
	phi = averagedegrees/(averagedegrees + 1)
	r = random.random() #random.random returns a random number between 0 and 1
	if r > phi:
		j = random.randint(0, len(DNETWORK) - 1)
		DNETWORK[j].append(i)
		AVERAGEACCUMULATOR.accumulateValues(1, 1)

	if r < phi:
		AVERAGEOUTDEGREE = 1
		TOTALNODECOUNT = len(DNETWORK)
		INTERVALVALUE = round(r * (TOTALNODECOUNT * AVERAGEOUTDEGREE))
		for destinationnode in DNETWORK.values():
			INDEGREECOUNT = len(destinationnode)
			if INDEGREECOUNT >= INTERVALVALUE:
				if len(NODETOATTACHTO) == 0:
					NODETOATTACHTO = destinationnode
				if INDEGREECOUNT <= len(NODETOATTACHTO):
					NODETOATTACHTO = destinationnode

		NODETOATTACHTO.append(i)
		AVERAGEACCUMULATOR.accumulateValues(1, 1)
		NODETOATTACHTO = []


DEGREE_THRESHOLD = 1

G = nx.DiGraph(DNETWORK)
NUMBER_OF_NODES = nx.number_of_nodes(G)

DEGREE_SEQUENCE = sorted(nx.degree(G, nbunch=None, weight=None).values(), reverse=True)
A = sorted([degree for degree in np.asarray(DEGREE_SEQUENCE) if degree >= DEGREE_THRESHOLD], reverse=True)

DEGREE_LOG_VALUES = []
RANK_LOG_VALUES = []
for f in A:
    RANK_LOG_VALUES.append(math.log(A.index(f)+1/NUMBER_OF_NODES))
    DEGREE_LOG_VALUES.append(math.log(f))

SLOPE, INTERCEPT, R_VALUE, P_VALUE, SLOPE_STD_ERROR = stats.linregress(DEGREE_LOG_VALUES, RANK_LOG_VALUES)

print("Slope ", SLOPE)
print("Y-intercept ", INTERCEPT)
print("Alpha ", calculatealpha(SLOPE))

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
plt.title("Price Model Synthetic Network Degree Distribution")
plt.ylabel("Log Rank")
plt.xlabel("Log Degree")
pyl.show()
