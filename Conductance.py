import math
import numpy as np
import scipy.io
import scipy as sp
import pandas as pd


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
    conductance = math.inf
    size = len(A)
    # GIVES US BINARY ARRAY
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


def findConductanceMat (A):
    conductance = math.inf
    size = len(A)
    # GIVES US BINARY ARRAY
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
                if A[one, zero] != 0:
                    capacity += A[one, zero]

        if capacity < conductance:
            conductance = capacity
    return conductance


# theConductance = findConductance(Adj)
# print("Conductance", theConductance)

mat = scipy.io.loadmat('GD06_theory.mat')
matrix = mat['Problem']['A'][0][0]

# dense matrix
denseMatrix = matrix.todense()

theConductance = findConductanceMat(denseMatrix)
print(theConductance)













