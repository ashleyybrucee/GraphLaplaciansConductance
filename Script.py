import numpy as np
import math
from scipy.sparse import csgraph
from datetime import datetime
import A9s
import Laplacians

def diag (A):
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


    #normA = Diag * A * Diag
    normA = Diag @ A @ Diag
    I = np.identity(len(A))
    normLbynormA = I - normA
    #normLbyDA = Diag * (D - A) * Diag
    #normLbyL = Diag * L * Diag

    normLbyDA = Diag @ (D - A) @ Diag
    normLbyL = Diag @ L @ Diag

    print(normLbynormA)
    print(normLbyDA)
    print (normLbyL)

    return normLbyL




diag(Laplacians.ours_4)
#diag(A9s.nine_1)