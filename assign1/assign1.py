import math

class binomialTree:
    def __init__(self, depth, strike_price, start, interest, volatility, maturity):
        self.tree = []
        self.u = 1 + volatility
        self.d = 1 - volatility
        self.r = interest
        self.T = maturity
        self.step = depth
        self.start = start
        for i in range(self.step):
            price = start*self.u**(self.step-1-i)*self.d**i
            payoff = price - strike_price
            if(payoff < 0):
                payoff = 0
            startnode = node(price, payoff)
            self.tree.append(startnode)

    def tree_step(self):
        self.step -= 1
        new_tree = []
        for i in range(self.step):
            upstate = self.tree[i]
            downstate = self.tree[i+1]
            delta = (upstate.payoff - downstate.payoff) / (upstate.price - downstate.price)
            portfolio_price = delta*upstate.price - upstate.payoff
            portfolio_PV = portfolio_price * math.e**(-self.r*self.T)
            price = self.start*self.u**(self.step-1-i)*self.d**i
            newNode = node(price, portfolio_PV)
            new_tree.append(newNode)

        self.tree = new_tree

        if(self.step == 1):
            print("Value of option: ", delta*self.start - portfolio_PV)

    def run_model(self):
        while(self.step > 1):
            self.tree_step();

    def print_tree(self):
        for i in range(len(self.tree)):
            print(self.tree[i].price, self.tree[i].payoff)


class node:
    def __init__(self, S, payoff):
        self.price = S
        self.payoff = payoff

if __name__ == '__main__':
    BT = binomialTree(50, 99, 100, 0.06, 0.2, 1)
    BT.print_tree()
    BT.run_model()
