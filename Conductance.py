import math
import numpy as np
import scipy.io
import scipy.linalg as linalg
from datetime import datetime
from scipy.sparse import csgraph

import A9s
import Laplacians

# helper function to determine binary set partitioning
def printBinNum (binNums):
    if len(binNums) == 1:
        print("000" + binNums)
    elif len(binNums) == 2:
        print("00" + binNums)
    elif len(binNums) == 3:
        print("0" + binNums)
    else:
        print(binNums)

# helper function to count number of edges in a graph
def calcEdgeNumber (A):
    size = len(A)
    edges = 0
    for i in range (size):
        for j in range (i, size):
            edges = edges + A[i][j]
    return edges

# returns the min degree between two sets
def setDegrees (L, setA, setB):
    edgeA = 0
    edgeB = 0
    for node in setA:
        edgeA = edgeA + L[node, node]
    for node in setB:
        edgeB = edgeB + L[node, node]

    return min(edgeA, edgeB)

# calculates isoperimetric ratio
def findisoR (A):
    isoR = math.inf
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

        if capacity < isoR:
            isoR = capacity
    return isoR

def isoWithMatrix (A):
    ANp = np.array(A)
    now = datetime.now()
    print("Start IsoR:", now.strftime("%H:%M:%S"))
    isoR = findisoR(ANp)
    now = datetime.now()
    print("End IsoR:", now.strftime("%H:%M:%S"))
    print("IsoR", isoR)
def isoWithMatFile (A):
    mat = scipy.io.loadmat(A)
    matrix = mat['Problem']['A'][0][0]
    denseMatrix = matrix.todense()
    print(denseMatrix)

    now = datetime.now()
    print("Start IsoR:", now.strftime("%H:%M:%S"))
    isoR = findisoR(denseMatrix)
    now = datetime.now()
    print("End IsoR:", now.strftime("%H:%M:%S"))
    print(isoR)

# calculates Fiedler vector, with Adjacency or Laplacian
def fiedlerValA(A):
    if (type (A) != 'numpy.matrix'):
        # print ("converting from ",type(A))
        A = np.matrix(A)
    # print ("now type ",type(A))
    # convert to Laplacian
    L = csgraph.laplacian(A)
    eig_vals, eig_vex = linalg.eig(L)
    fiedler_val = np.sort(eig_vals.real)[1]
    print(eig_vals)
    return fiedler_val
def fiedlerValL(L):
    eig_vals, eig_vex = linalg.eig(L)
    fiedler_val = np.sort(eig_vals.real)[1]
    print(eig_vals)
    return fiedler_val

# calculates the normalized laplacian
def normalizedLaplacian(A):
    if type(A) != 'numpy.matrix':
        A = np.matrix(A)

    # gets diagonal from laplacian
    L = csgraph.laplacian(A)
    Diag = np.zeros(A.shape)
    D = np.diag(L)
    np.fill_diagonal(Diag, D)

    D = np.copy(Diag)

    # calculated normalized degree matrix
    for i in range(len(A)):
        currVal = Diag[i, i]
        sqrtVal = math.sqrt(currVal)
        Diag[i, i] = 1 / sqrtVal

    # three different ways to calculate the normalized Laplacian
    normA = Diag @ A @ Diag
    I = np.identity(len(A))
    normLbynormA = I - normA

    normLbyDA = Diag @ (D - A) @ Diag

    normLbyL = Diag @ L @ Diag

    return normLbyL

# calculates the Cheeger's inequality for conductance approximation
def findCondApprox (A):
    now = datetime.now()
    print("Start Fiedler Approx:", now.strftime("%H:%M:%S"))
    L = normalizedLaplacian(A)
    fVal = fiedlerValL(L)
    lowerBound = fVal / 2
    upperBound = math.sqrt(2 * fVal)
    now = datetime.now()
    print("End Fiedler Approx:", now.strftime("%H:%M:%S"))
    print("Fiedler", fVal)
    print("Lower", lowerBound)
    print("Upper", upperBound)

# finds the conductance of a graph
def findCond (A):
    conductance = math.inf
    size = len(A)
    # GIVES US BINARY ARRAY
    numPartitions = 2 ** (size - 1)
    for i in range(1, numPartitions):
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

        L = csgraph.laplacian(A)
        minEdges = setDegrees(L, ones, zeros)
        if len(ones) < len(zeros):
            capacity = capacity / minEdges
        else:
            capacity = capacity / minEdges

        if capacity < conductance:
            conductance = capacity
    return conductance

def condWithMatrix (A):
    ANp = np.array(A)
    now = datetime.now()
    print("Start Cond:", now.strftime("%H:%M:%S"))
    theConductance = findCond(ANp)
    now = datetime.now()
    print("End Cond:", now.strftime("%H:%M:%S"))
    print("Cond", theConductance)
def condWithMatFile (A):
    mat = scipy.io.loadmat(A)
    matrix = mat['Problem']['A'][0][0]
    denseMatrix = matrix.todense()
    print(denseMatrix)

    now = datetime.now()
    print("Start Cond:", now.strftime("%H:%M:%S"))
    theConductance = findCond(denseMatrix)
    now = datetime.now()
    print("End Cond:", now.strftime("%H:%M:%S"))
    print(theConductance)
