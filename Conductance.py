import math
import numpy as np

Adj = [[0, 1, 1, 0],
     [1, 0, 1, 1],
     [1, 1, 0, 1],
     [0, 1, 1, 0]]


def printBinNum (binNum):
    if len(binNums) == 1:
        print("000" + binNums)
    elif len(binNums) == 2:
        print("00" + binNums)
    elif len(binNums) == 3:
        print("0" + binNums)
    else:
        print(binNums)


def findConductance (A):
    # GIVES US BINARY ARRAY
    conductance = math.inf
    size = len(A)
    numPartitions = 2 ** (size - 1)
    for i in range (1, numPartitions):
        binArray = np.zeros(size)
        binString = str(bin(i))
        binNums = binString[2:]
        counter = len(binArray) - 1
        for digit in reversed(binNums):
            binArray[counter] = int(digit)
            counter -= 1

        # SET PARTITIONING
        ones = []
        zeros = []
        for j in range(len(binArray)):
            if binArray[j] == 1:
                ones.append(j)
            else:
                zeros.append(j)

        capacity = 0
        for one in ones:
            for zero in zeros:
                if A[one][zero] != 0:
                    capacity += A[one][zero]

        if capacity < conductance:
            conductance = capacity
    return conductance


theConductance = findConductance(Adj)
print("Conductance", theConductance)








