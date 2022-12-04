from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import math


@dataclass
class BlackScholes:
    spot: float = 100
    strike: float = 100
    maturity: float = 1
    risk_free_rate: float = 0.05
    volatility: float = 0.3
    dividend: float = 0

    def d1(self) -> float:
        return (np.log(self.spot / self.strike) + (self.risk_free_rate - self.dividend + self.volatility ** 2 / 2) *
                self.maturity) / (self.volatility * np.sqrt(self.maturity))

    def d2(self) -> float:
        return self.d1() - self.volatility * np.sqrt(self.maturity)


    def call_value(self) -> float:
        return self.spot * np.exp(-self.dividend * self.maturity) * norm.cdf(self.d1(), 0, 1) - \
               self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(self.d2(), 0, 1)


    def put_value(self) -> float:
        return self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(-self.d2(), 0, 1) - \
               self.spot * np.exp(-self.dividend * self.maturity) * norm.cdf(-self.d1(), 0, 1)

    def delta_call(self) -> float:
        return norm.cdf(self.d1(), 0, 1)

    def delta_put(self) -> float:
        return - norm.cdf(-self.d1())

    def gamma(self) -> float:
        return norm.pdf(self.d1()) / (self.spot * self.volatility * np.sqrt(self.maturity))

    def vega(self) -> float:
        return self.spot * np.sqrt(self.maturity) * norm.pdf(self.d1()) * 0.01

    def theta_call(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) -
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) *
                  norm.cdf(self.d2())) / 365

    def theta_put(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) +
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) *
                  norm.cdf(-self.d2())) / 365

    def rho_call(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) -
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(
                    self.d2())) / 100

    def rho_put(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) +
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(
                    self.d2())) / 100

    def get_plot(self):
        plt.style.use('dark_background')

        # price/spot
        S = np.arange(60,  140, 0.1)
        calls = [BlackScholes(spot=s).call_value() for s in S]
        puts = [BlackScholes(spot=s).put_value() for s in S]

        # Initialise the subplot function using number of rows and columns
        figure, axis = plt.subplots(2, 2)

        # price/volatility
        axis[0, 0].plot(S, calls, label='Call Value')
        axis[0, 0].plot(S, puts, label='Put Value')
        axis[0, 0].set_title("Call and Put Value / Spot")
        plt.xlabel('$\sigma$')

        sigmas = np.arange(0.1, 1.5, 0.01)
        calls = [BlackScholes(volatility=sigma).call_value() for sigma in sigmas]
        puts = [BlackScholes(volatility=sigma).put_value() for sigma in sigmas]


        # price/maturity
        l1 = axis[0, 1].plot(sigmas, calls, label='Call Value')
        l2 = axis[0, 1].plot(sigmas, puts, label='Put Value')
        axis[0, 1].set_title("Call and Put Value / Volatility")
        plt.xlabel('$\sigma$')

        T = np.arange(0, 2, 0.01)
        l3 = calls = [BlackScholes(maturity=t).call_value() for t in T]
        l4 = puts = [BlackScholes(maturity=t).put_value() for t in T]

        # For Tangent Function
        l5 = axis[1, 0].plot(T, calls)
        l6 = axis[1, 0].plot(T, puts)
        axis[1, 0].set_title("Call and Put Value / Time")
        plt.xlabel('a')

        # price/
        R = np.arange(0, 0.5, 0.001)
        calls = [BlackScholes(risk_free_rate=r).call_value() for r in R]
        puts = [BlackScholes(risk_free_rate=r).put_value() for r in R]


        axis[1, 1].plot(R, calls)
        axis[1, 1].plot(R, puts)
        axis[1, 1].set_title("Call and Put Value / risk free rate")


        axis[0, 0].set(xlabel='$S_0$', ylabel='Value')
        axis[0, 1].set(xlabel='$\sigma$', ylabel='Value')
        axis[1, 0].set(xlabel='$T$ in years', ylabel='Value')
        axis[1, 1].set(xlabel='$r$', ylabel='Value')

        plt.show()