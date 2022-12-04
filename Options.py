from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


@dataclass
class BlackScholes:
    spot: float = 100
    strike: float = 100
    maturity: float = 1
    risk_free_rate: float = 0.05
    volatility: float = 0.3
    dividend: float = 0

    def d1(self) -> float:
        return (np.log(self.spot / self.strike) + (self.risk_free_rate - self.dividend + self.volatility ** 2 / 2) * \
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
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) -\
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) *\
                  norm.cdf(self.d2())) / 365

    def theta_put(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) +\
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) *\
                  norm.cdf(-self.d2())) / 365

    def rho_call(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) -\
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(
                    self.d2())) / 100

    def rho_put(self) -> float:
        return - (self.spot * norm.pdf(self.d1()) * self.volatility / (2 * np.sqrt(self.maturity)) +\
                  self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(
                    self.d2())) / 100

