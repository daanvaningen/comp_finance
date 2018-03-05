import math
import numpy
import scipy
from tqdm import tqdm

def max(a,b):
    if(a > b):
        return a
    return b

def arithmeticAsianCallValue (S0, K, v, r, T, N, M):

    dt = T*1.0/N
    drift = math.exp((r-0.5*v*v)*dt)

    Spath = numpy.empty(N, dtype=float)
    arithPayOff = numpy.empty(M, dtype=float)

    for i in range(0,M,1):
        growthFactor = drift * math.exp(v*math.sqrt(dt)*numpy.random.normal())
        Spath[0] = S0 * growthFactor
        for j in range(1,N,1):
            growthFactor = drift * math.exp(v*math.sqrt(dt)*numpy.random.normal())
            Spath[j] = Spath[j-1] * growthFactor

        arithMean = numpy.mean(Spath)
        arithPayOff[i] = math.exp(-r*T)* max(arithMean-K, 0)

    # Standard Monte Carlo
    Pmean = numpy.mean(arithPayOff)
    Pstd = numpy.std(arithPayOff)

    confmc = [Pmean-1.96*Pstd/math.sqrt(M), Pmean+1.96*Pstd/math.sqrt(M)]

    return Pmean, confmc

values = []
for _ in range(10):
	mean, interval = arithmeticAsianCallValue(99, 100, 0.2, 0.06, 1, 50, 1000)
	values.append(mean)
print(values)
print((0.06 - 0.1)*(50-1)/100)
