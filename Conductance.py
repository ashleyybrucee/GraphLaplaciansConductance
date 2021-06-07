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
    print("Start Conductance:", now.strftime("%H:%M:%S"))
    theConductance = findConductance(ANp)
    now = datetime.now()
    print("End Conductance:", now.strftime("%H:%M:%S"))
    print("Conductance", theConductance)

def calcWithMatFile (A):
    mat = scipy.io.loadmat(A)
    matrix = mat['Problem']['A'][0][0]
    denseMatrix = matrix.todense()
    print(denseMatrix)

    now = datetime.now()
    print("Start Conductance:", now.strftime("%H:%M:%S"))
    theConductance = findConductanceMat(denseMatrix)
    now = datetime.now()
    print("End Conductance:", now.strftime("%H:%M:%S"))
    print(theConductance)

def fiedlerValA(A):
    if (type (A) != 'numpy.matrix'):
        print ("converting from ",type(A))
        A = np.matrix(A)
    print ("now type ",type(A))
    # convert to Laplacian
    L = csgraph.laplacian(A)
    eig_vals, eig_vex = linalg.eig(L)
    fiedler_val = np.sort(eig_vals.real)[1]
    return fiedler_val

def fiedlerValL(L):
    eig_vals, eig_vex = linalg.eig(L)
    fiedler_val = np.sort(eig_vals.real)[1]
    return fiedler_val

def normalizedLaplacian (A):
    if type (A) != 'numpy.matrix':
        A = np.matrix(A)

    # gets diagonal from laplacian
    L = csgraph.laplacian(A)
    Diag = np.zeros(A.shape)
    D = np.diag (L)
    np.fill_diagonal(Diag, D)

    D = np.copy(Diag)

    # calculated normalized degree matrix
    for i in range (len(A)):
        currVal = Diag[i, i]
        sqrtVal = math.sqrt(currVal)
        Diag[i, i] = 1 / sqrtVal

    # calculates normalized laplacian
    normA = Diag * A * Diag
    I = np.identity(len(A))
    normL = I - normA

    return normL

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

def nonNormalizedBounds(A):
    fVal = fiedlerValA(A)
    print(fVal)
    lowerBound = fVal / 2
    upperBound = math.sqrt(2 * fVal)
    print("Lower", lowerBound)
    print("Upper", upperBound)








