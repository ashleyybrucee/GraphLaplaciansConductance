import math
import numpy as np
import scipy.io
import scipy.linalg as linalg
from datetime import datetime
from scipy.sparse import csgraph

def printBinNum (binNums):
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

        if len(ones) < len(zeros):
            capacity = capacity / len(ones)
        else:
            capacity = capacity / len(zeros)

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

        if len(ones) < len(zeros):
            capacity = capacity / len(ones)
        else:
            capacity = capacity / len(zeros)

        if capacity < conductance:
            conductance = capacity
    return conductance

def calcWithMatrix (A):
    ANp = np.array(A)
    now = datetime.now()
    print(now.strftime("%H:%M:%S"))
    theConductance = findConductance(ANp)
    now = datetime.now()
    print(now.strftime("%H:%M:%S"))
    print("Conductance", theConductance)


def calcWithMatFile (A):
    mat = scipy.io.loadmat(A)
    matrix = mat['Problem']['A'][0][0]
    denseMatrix = matrix.todense()
    print(denseMatrix)

    now = datetime.now()
    print(now.strftime("%H:%M:%S"))
    theConductance = findConductanceMat(denseMatrix)
    now = datetime.now()
    print(now.strftime("%H:%M:%S"))
    print(theConductance)

'''
Pass an adjacency matrix to this function to get the Fiedler val
Make sure not to pass a Laplacian, since it will try to convert it
and the resulting matrix won't be accurate
'''
def fiedlerVal(A):
    if(type(A)!= 'numpy.matrix'):
        print("converting from ",type(A))
        A = np.matrix(A)
    print("now type ",type(A))
    #convert to Laplacian
    L = csgraph.laplacian(A)
    eig_vals, eig_vex = linalg.eig(L)
    fiedler_val = np.sort(eig_vals.real)[1]
    return fiedler_val

'''
# CONDUCTANCE FOR BASIC GRAPH
now = datetime.now()
print(now.strftime("%H:%M:%S"))
theConductance = findConductance(ours_9)
print(now.strftime("%H:%M:%S"))
print("Conductance", theConductance)
###

# CONDUCTANCE FOR MAT GRAPH
mat = scipy.io.loadmat('file.mat')
matrix = mat['Problem']['A'][0][0]
denseMatrix = matrix.todense()
print(denseMatrix)

now = datetime.now()
print(now.strftime("%H:%M:%S"))
theConductance = findConductanceMat(denseMatrix)
now = datetime.now()
print(now.strftime("%H:%M:%S"))
print(theConductance)

'''
