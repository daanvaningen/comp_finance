import math
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import time

american = False

def max(a,b):
    if(a > b):
        return a
    return b

class binomialTree:
    def __init__(self, depth, strike_price, start,
                    interest, volatility, maturity, option_type="call"):
        self.tree = [] # array that stores the 'tree nodes' per iteration
        self.step = depth + 1 # 3th level 4 nodes 4th level 5 nodes etc.
        self.dt = float(maturity)/depth # delta t, timestep size
        self.start = start # start price of stock
        self.strike_price = strike_price # strike price
        self.u = math.e**(volatility*math.sqrt(1.0/depth)) # up factor
        self.d = 1/self.u # down factor
        self.r = interest # interest rate
        self.volatility = volatility
        self.T = maturity # maturity of the stock
        self.type = option_type # call or put option
        # up or down probability
        self.p = (math.e**(self.r*self.dt) - self.d)/(self.u - self.d)
        # Initialize nodes and payoffs
        for i in range(self.step):
            price = self.start*self.u**(self.step-1-i)*self.d**i
            payoff = self.determine_option_value(price, self.strike_price,self.type)
            startnode = node(price, payoff)
            self.tree.append(startnode)

    def tree_step(self):
        self.step -= 1
        new_tree = []
        for i in range(self.step):
            upstate = self.tree[i]
            downstate = self.tree[i+1]
            # calculate price of new node via direct formula
            price = self.start*self.u**(self.step-1-i)*self.d**i
            # risk free price of option at that node
            f = (self.p*upstate.payoff + (1 - self.p)*
                downstate.payoff)*math.e**(-self.r*self.dt)
            if(american and self.type == "call"):
                f = max(f, price - self.strike_price)
            elif(american and self.type != "call"):
                f = max(f, self.strike_price - price)
            delta = (upstate.payoff - downstate.payoff) / (upstate.price - downstate.price)
            new_node = node(price, f, delta)
            new_tree.append(new_node)

        self.tree = new_tree # replace old nodes

    def run_model(self):
        # run model untill there is only one node
        while(self.step > 1):
            # self.print_tree()
            self.tree_step();

        return self.tree[0]

    def determine_option_value(self, S, K, type):
        if(type == "call"):
            value = S - K
            if(value > 0):
                return value
            else:
                return 0
        else:
            value = K - S
            if(value > 0):
                return value
            else:
                return 0

    def print_tree(self):
        for i in range(len(self.tree)):
            print(self.tree[i].price, self.tree[i].payoff)

    def black_scholes(self):
        # https://www.investopedia.com/university/options-pricing/black-scholes-model.asp
        d1 = (math.log(self.start/self.strike_price)+ \
                        (self.r+0.5*self.volatility**2)*self.T)/\
                        (self.volatility*math.sqrt(self.T))
        d2 = d1 - self.volatility * math.sqrt(self.T)
        C = self.start*norm.cdf(d1) - \
            norm.cdf(d2) * self.strike_price * math.e**(-self.r*self.T)
        return C, d1, d2

class node:
    def __init__(self, S, payoff, delta=0):
        self.price = S
        self.payoff = payoff
        self.delta = delta

def accuracy_analysis(analytical_value):
    estimates = []
    for i in range(2,100):
        BT = binomialTree(i, 99, 100, 0.06, 0.2, 1.0)
        estimate = BT.run_model()
        estimates.append(abs(estimate.payoff-analytical_value))

    plt.figure()
    plt.xlabel("tree depth")
    plt.ylabel("Absolute error")
    plt.title("Absolute error vs binomial tree depth")
    # plt.yscale('log')
    plt.plot(estimates)
    plt.show()

class hedging_simulation:
    def __init__(self, r, S, dt, sigma, delta):
        self.r = r
        self.S = S
        self.dt = dt/365.0
        self.sigma = sigma
        self.delta = delta

    def run_sim(self):
        values = []
        randoms = np.random.normal(0, 1, 10000)
        for random in randoms:
            S = self.r*self.S*self.dt + self.sigma*self.S*random*math.sqrt(self.dt)
            values.append(S)

        plt.figure()
        plt.hist(randoms, edgecolor='black', bins=50)
        plt.show()

def volatility_influence():
    values = []
    for i in range(1,101):
        BT = binomialTree(50, 99, 100, 0.06, i/100.0, 1.0, option_type='put')
        BT = binomialTree(50, 99, 100, 0.06, i/100.0, 1.0, option_type='p')
        analytical_value, d1, d2 = BT.black_scholes()
        estimate = BT.run_model()
        values.append(abs(estimate.payoff))

    plt.figure()
    plt.xlabel("Volatility")
    plt.ylabel("Price")
    plt.title("Price vs volatility European put option")
    plt.xlabel("volatility")
    plt.ylabel("Absolute error")
    plt.title("Absolute error vs volatility American put option")
    plt.plot(values)
    plt.show()

def complexity_analysis():
    values = []
    for i in range(1, 500):
        BT = binomialTree(i, 99, 100, 0.06, 0.2, 1.0)
        time1 = time.time()
        BT.run_model()
        values.append(time.time() - time1)

    plt.figure()
    plt.plot(values)
    plt.xlabel('Tree depth')
    plt.ylabel('Time (s)')
    plt.title('complexity analysis tree depth and execution time')
    plt.show()

def hedge_parameter_analysis():
    BT_hedge = []
    analytical_value = []
    x = []
    for i in range(1, 101, 2):
        x.append(i)
        BT = binomialTree(50, 99, 100, 0.06, i/100.0, 1.0)
        node = BT.run_model()
        C, d1, d2 = BT.black_scholes()
        analytical_value.append(norm.cdf(d1))
        BT_hedge.append( node.delta)

    plt.figure()
    plt.title('Comparison Hedge paramater and analytical value')
    plt.xlabel('Volatility')
    plt.ylabel('Delta')
    plt.plot(x, BT_hedge, 'r--', label="BT hedge value")
    plt.plot(x, analytical_value, 'b.', label="analytical value")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # complexity_analysis()
<<<<<<< HEAD
    hedge_parameter_analysis()
    american = False
    volatility_influence()
    BT = binomialTree(6, 99, 100, 0.06, 0.2, 1.0, option_type='c')
=======
    # hedge_parameter_analysis()
    american = True
    # volatility_influence()
    BT = binomialTree(6, 99, 100, 0.06, 0.2, 1.0, option_type='p')
>>>>>>> bdf19c8529acd0929f93d7c9f483b89ea751d641
    C, d1, d2 = BT.black_scholes()
    estimate = BT.run_model()
    print(estimate.payoff, C)
