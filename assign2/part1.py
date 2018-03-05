import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
from tqdm import tqdm

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
        self.T = maturity
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

    def black_scholes(self):
        # https://www.investopedia.com/university/options-pricing/black-scholes-model.asp
        d1 = (math.log(self.S/self.K)+ \
                        (self.r+0.5*self.vol**2)*self.T)/\
                        (self.vol*math.sqrt(self.T))
        d2 = d1 - self.vol * math.sqrt(self.T)
        C = self.S*norm.cdf(d1) - \
            norm.cdf(d2) * self.K * math.e**(-self.r*self.T)

        P = C + self.K*math.e**(-self.r*self.T) - self.S
        return P

    def convergence(self, trials, reps):
        trials = [100*i for i in range(1, trials)]
        total = []
        RV = 16.273
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


# def strike_influence():
#     strikes = [50 + 5*i for i in range(10)]
#     reps = 100
#     total = []
#     print(strikes)
#     for strike in strikes:
#         print strike
#         opt = Option(strike, 100, 0.06, 0.2, 1, 365)
#         C = opt.black_scholes()
#         values = []
#         for _ in range(reps):
#             values.append(opt.option_price(reps) - C)
#         total.append(values)
#
#     avgs = []
#     stds = []
#     print(len(total))
#     for i in range(len(total)):
#         col = [row[i] for row in total]
#         avgs.append(np.mean(col))
#         stds.append(np.std(col))
#
#     fig, ax = plt.subplots(1)
#     ax.plot(strikes, avgs, color="blue", label="mean")
#     ax.fill_between(strikes, [avgs[i] + stds[i] for i in range(len(total))],
#                     [avgs[i] - stds[i] for i in range(len(total))], color="blue", alpha=0.4, label="68% interval")
#     ax.fill_between(strikes, [avgs[i] + 2*stds[i] for i in range(len(total))],
#                     [avgs[i] - 2*stds[i] for i in range(len(total))], color="blue", alpha=0.2, label="95% interval")
#
#     plt.title("Accuracy of MC depending on the strike price")
#     plt.ylabel("MC error")
#     plt.xlabel("Strike price")
#     ax.legend()
#     # plt.xscale('log')
#     plt.show()
#

if __name__ == '__main__':

    # opt = Option(99, 100, 0.06, 0.2, 1, 365)
    # opt.convergence(15, 20)
    # strike_influence()
    opt = Option(120, 100, 0.06, 0.2, 1, 365)
    opt.convergence(15, 20)

    # opt = Option(60, 100, 0.06, 0.2, 1, 365)
    # opt.convergence(15, 20)
