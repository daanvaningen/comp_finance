import numpy as np
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
from scipy.stats import norm

# Returns the stock price at time T
def S_T(T, r, S, Volatility, Epsilon1):
    return S*math.exp((r-0.5*Volatility**2)*T + Volatility*Epsilon1*math.sqrt(T))

# The digital option function
def DigitalOption(St, K):
    if (K - St) < 0:
        return 1
    else:
        return 0
    
def HedgeCalculator1(Num_Sim, T, K, r, S, Volatility, Iterations, Epsilon, Same_Seed = False):
    # Keeps track of the different simulation and their hedge value
    Total_hedges = []

    # Loop over all simulations *default = 8*
    for iterate in range(Num_Sim):
        # If we want the same seed then it is calculated and stored here.
        if Same_Seed:
            x = np.random.randint(100)
            random.seed(x)

        # Calculate V bumped.
        V_bumped = []
        for i in range(Iterations):
            St = S_T(i/float(Iterations)*T, r, S+Epsilon, Volatility, random.normalvariate(0, 1))
            V_bumped.append(max(K-St, 0))

        V_B = math.exp(-r*T)*(sum(V_bumped)/float(Iterations))

        # Setting random seed to x if it should be the same
        if Same_Seed:
            random.seed(x)
        
        # Calculate V unbumped
        V_unbumped = []
        for i in range(Iterations):
            St = S_T(i/float(Iterations)*T, r, S, Volatility, random.normalvariate(0,1))
            V_unbumped.append(max(K-St, 0))

        V_U = math.exp(-r*T)*(sum(V_unbumped)/float(Iterations))

        # Calculate the hedge and add it to the lists of all hedge simulations
        hedge = (V_B - V_U)/Epsilon
        Total_hedges.append(hedge)

    # Return the mean hedge value of all simulations
    return np.mean(Total_hedges)

def HedgeCalculator2(Num_Sim, T, K, r, S, Volatility, Iterations, Epsilon, Same_Seed = False):
    Total_hedges = []
    for iterate in range(Num_Sim):
        if Same_Seed:
            x = np.random.randint(100)
            random.seed(x)

        # Calculate V bumped.
        V_bumped = []
        for i in range(Iterations):
            St = S_T(i/float(Iterations)*T, r, S+Epsilon, Volatility, random.normalvariate(0, 1))
            V_bumped.append(DigitalOption(St,K))

        V_B = math.exp(-r*T)*(sum(V_bumped)/float(Iterations))

        # Setting random seed to 1, will be same if same_seed and otherwise be different from seed(2).
        if Same_Seed:
            random.seed(x)
        
        #    Calculate V unbumped
        V_unbumped = []
        for i in range(Iterations):
            St = S_T(i/float(Iterations)*T, r, S, Volatility, random.normalvariate(0,1))
            V_unbumped.append(DigitalOption(St, K))

        V_U = math.exp(-r*T)*(sum(V_unbumped)/float(Iterations))

        hedge = (V_B - V_U)/Epsilon
        Total_hedges.append(hedge)


    return np.mean(Total_hedges)

def HedgePlot(Same_Seed):
    # Setting the parameters for our experiment
    T = 1
    K = 99
    r = 0.06
    S = 100
    Volatility = 0.2
    Iterations = 10000
    Num_Sim = 8
    
    # d1 calculation as blacksholes
    d1 = (math.log(S/99.0)+ \
                        (r+0.5*Volatility**2)*T)/\
                        (Volatility*math.sqrt(T))

    Delta = norm.cdf(d1)-1

    # X and Y lists for the plot
    hedge = []
    Epsi = []
    for j in range(1, 100):
        Epsilon = j/100.0 * 0.5 + 0.01
        hedge.append((abs(HedgeCalculator1(8, T,K,r, S, Volatility, Iterations, Epsilon, Same_Seed)-Delta))/abs(Delta) * 100)
        Epsi.append(Epsilon)

    if Same_Seed:
        plt.title("Same Seed")
    else:
        plt.title("Different Seed")
        
    plt.plot(Epsi, hedge)
    plt.xlabel("Epsilon")
    plt.ylabel("Relative error of Δ")
    plt.show()





# Here we do all the calculations and the plots, like a main function

HedgePlot(True)
HedgePlot(False)
print(HedgeCalculator1(8, 1, 99, 0.06, 100, 0.2, 10000, 0.1, True))


# _____ Following code is to calculate digital option ____ 

print(HedgeCalculator2(8, 1, 99, 0.06, 100, 0.2, 10000, 0.5, True))
print(HedgeCalculator2(8, 1, 99, 0.06, 100, 0.2, 10000, 0.01, True))
print(HedgeCalculator2(8, 1, 99, 0.06, 100, 0.2, 10000, 0.001, True))
