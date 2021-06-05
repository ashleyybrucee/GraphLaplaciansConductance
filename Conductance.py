import math
import numpy as np

def printBinNum (binNum):
    if len(binNums) == 1:
        print("000" + binNums)
    elif len(binNums) == 2:
        print("00" + binNums)
    elif len(binNums) == 3:
        print("0" + binNums)
    else:
        print(binNums)

A = [[0, 1, 1, 0],
     [1, 0, 1, 1],
     [1, 1, 0, 1],
     [0, 1, 1, 0]]

size = len(A)

conductance = math.inf

# GIVES US BINARY ARRAY
numPartitions = 2 ** (size - 1)
for i in range (1, numPartitions):
    binArray = np.zeros(size)
    binString = str(bin(i))
    binNums = binString[2:]
    #printBinNum (binNums)
    counter = len(binArray) - 1
    for digit in reversed(binNums):
        binArray[counter] = int(digit)
        counter -= 1

    #print("binArray", binArray)

    # separating the set indices into arrays
    ones = []
    zeros = []
    for j in range(len(binArray)):
        if binArray[j] == 1:
            ones.append(j)
        else:
            zeros.append(j)
    #print(ones)
    #print(zeros)
    
    #print("bin array", binArray)
    capacity = 0
    for one in ones:
        for zero in zeros:
            if A[one][zero] != 0:
                capacity += A[one][zero]
    print("Capacity", capacity)
    if capacity < conductance:
        conductance = capacity

print("Conductance", conductance)








