import numpy as np
import math
import matplotlib.pyplot as plt
from tqdm import tqdm

RV = 4.584

def max(a,b):
    if(a > b):
        return a
    return b

class Option:
    def __init__(self, K, S, r, vol, maturity, steps):
        self.K = K
        self.S = S
        self.r = r
        self.vol = vol
        self.maturity = maturity
        self.dt = float(maturity)/steps

    def euler(self, S):
        return S + S*(self.r*self.dt + self.vol*np.random.normal()*math.sqrt(self.dt))

    def run_sim(self, steps):
        S0 = self.S
        for _ in range(steps):
            S0 = self.euler(S0)
        return S0

    def option_price(self, M):
        values = []
        for _ in range(M):
            values.append(max(self.K - self.run_sim(365), 0))
        return sum(values)*math.e**(-self.r)/M

    def convergence(self, trials, reps):
        trials = [100*i for i in range(1, trials)]
        total = []
        for _ in tqdm(range(reps)):
            values = []
            for M in trials:
                values.append(self.option_price(M) - RV)
            total.append(values)

        avgs = []
        stds = []
        for i in range(len(trials)):
            col = [row[i] for row in total]
            avgs.append(np.mean(col))
            stds.append(np.std(col))

        fig, ax = plt.subplots(1)
        ax.plot(trials, avgs, color="blue", label="mean")
        ax.fill_between(trials, [avgs[i] + stds[i] for i in range(len(trials))],
                        [avgs[i] - stds[i] for i in range(len(trials))], color="blue", alpha=0.4, label="68% interval")
        ax.fill_between(trials, [avgs[i] + 2*stds[i] for i in range(len(trials))],
                        [avgs[i] - 2*stds[i] for i in range(len(trials))], color="blue", alpha=0.2, label="95% interval")

        plt.title("Convergence behaviour of Monte Carlo option pricing")
        plt.ylabel("MC error")
        plt.xlabel("Trials")
        ax.legend()
        # plt.xscale('log')
        plt.show()

if __name__ == '__main__':

    opt = Option(99, 100, 0.06, 0.2, 1, 365)
    opt.convergence(15, 20)
