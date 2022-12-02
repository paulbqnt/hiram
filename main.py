from scipy.stats import norm
import numpy as np


class BlackScholes:
    def __init__(self, spot, strike, maturity, risk_free_rate, volatility, dividend=0):
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.dividend = dividend

    def d1(self):
        return (np.log(self.spot / self.strike) + (self.risk_free_rate - self.dividend + self.volatility ** 2 / 2) * \
                self.maturity) / (self.volatility * np.sqrt(self.maturity))

    def d2(self):
        return self.d1() - self.volatility * np.sqrt(self.maturity)

    def call_value(self):
        return self.spot * np.exp(-self.dividend * self.maturity) * norm.cdf(self.d1()) - \
               self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(self.d2())

    def put_value(self):
        return self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(-self.d2()) - \
               self.spot * np.exp(-self.dividend * self.maturity) * norm.cdf(-self.d1())

    def delta_call(self):
        return norm.cdf(self.d1())

    def delta_put(self):
        return - norm.cdf(-self.d1())

    def gamma(self):
        return norm.pdf(self.d1()) / (self.spot * self.volatility * np.sqrt(self.maturity))


aapl = BlackScholes(spot=49, strike=50, maturity=0.3846, risk_free_rate=.05, volatility=0.2)

print(aapl.gamma_call())
