import numpy as np
from scipy.stats import norm, probplot
from typing import Optional
from pydantic import BaseModel, Field
from yahooquery import Ticker
from typing import Dict
from uuid import uuid4, UUID



class BlackScholes(BaseModel):
    '''
    The BlackScholes object contains methods to price Options

    Attributes:
        way: c/p (call or put)
        S: spot price
        K: strike price
        T: Maturity (in years)
        r: risk free rate (percentage)
        sigma: volatility (percentage)
        q: dividend
        qty: number of options
        price: price of the option
    '''
    #ticker: Optional[str] = None
    way: Optional[str] = 'c'
    S: float
    K: float
    T: float
    r: float
    sigma: float
    q: Optional[float] = 0
    qty: Optional[float] = 1
    price: Optional[float] = 1
    id_: UUID = Field(default_factory=uuid4)

    def get_price(self):
        return Ticker(self.ticker).summary_detail

    @property
    def currency(self):
        return Ticker(self.ticker).summary_detail.get('AAPL').get('currency')

    def d1(self):
        """Performs d1 computation of the Black Scholes Formula"""
        return (np.log(self.S / self.K) + (self.r - self.q + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        """Performs d2 computation of the Black Scholes Formula"""
        return self.d1() - self.sigma * np.sqrt(self.T)
    
    def value(self):
        if self.way == 'c':
            return self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1(), 0, 1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2(), 0, 1)
        elif self.way == 'p':
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2(), 0, 1) - self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1(), 0, 1)

    def delta(self):
        if self.way == 'c':
            return norm.cdf(self.d1(), 0, 1)
        elif self.way == 'p':
            return - norm.cdf(-self.d1())

    def gamma(self):
        """Return gamma level of the Option"""
        return norm.pdf(self.d1()) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        """Return vega level of the Option"""
        return self.S * np.sqrt(self.T) * norm.pdf(self.d1()) * 0.01

    def rho(self):
        if self.way == 'c':
            return - (self.S * norm.pdf(self.d1()) * self.sigma / (2 * np.sqrt(self.T)) -
                  self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(
            self.d2())) / 100

        elif self.way == 'p':
            return - (self.S * norm.pdf(self.d1()) * self.sigma / (2 * np.sqrt(self.T)) +
                  self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(
            self.d2())) / 100

    def theta(self):
        """Return theta level of the Option"""
        if self.way == 'c':
            return - (self.S * norm.pdf(self.d1()) * self.sigma / (2 * np.sqrt(self.T)) -
                    self.r * self.K * np.exp(-self.r * self.T) *
                    norm.cdf(self.d2())) / 365

        elif self.way == 'p':
            return - (self.S * norm.pdf(self.d1()) * self.sigma / (2 * np.sqrt(self.T)) +
                    self.r * self.K * np.exp(-self.r * self.T) *
                    norm.cdf(-self.d2())) / 365