"""This generates a synthetic network using Price's Model"""
import random
import pylab     # only if you want graphics
import utilities.average_accumulator as AvgAcc

DNETWORK = {}       # dictionary of lists
INODES = 10000      # total number of nodes
NODERANGE = range(INODES)
NODETOATTACHTO = []
COUNTER = 0

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
LDEGREES = sorted([len(node) for node in DNETWORK.values()], reverse=True)
#print(LDEGREES)

# and draw a histogram
pylab.hist(LDEGREES, 50)
pylab.xlabel("Node Degree")
pylab.ylabel("Number of Nodes")
pylab.title("Price Model Synthetic Network | Node Count: " + str(INODES))
pylab.show()
