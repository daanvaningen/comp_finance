import math

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
            new_node = node(price, f)
            new_tree.append(new_node)

        self.tree = new_tree # replace old nodes

    def run_model(self):
        # run model untill there is only one node
        while(self.step > 1):
            self.tree_step();

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


class node:
    def __init__(self, S, payoff):
        self.price = S
        self.payoff = payoff

if __name__ == '__main__':
    BT = binomialTree(50, 99, 100, 0.06, 0.2, 1.0)
    BT.run_model()
    BT.print_tree()
