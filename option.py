import numpy as np
from scipy.stats import norm, probplot
from typing import Optional
from pydantic import BaseModel, Field
from yahooquery import Ticker
from typing import Dict
from uuid import uuid4, UUID
from enum import Enum
import matplotlib.pyplot as plt




class Way(str, Enum):
    """Choose between c and p (call/put)"""
    c='c',
    p='p'


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
    #way: Optional[str] = 'c'
    way: Way
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
            rho_result = self.K * self.T * np.exp(-self.r *self.T) * norm.cdf(self.d2(), 0, 1)

        elif self.way == 'p':
            rho_result = -self.K * self.T * np.exp(-self.r *self.T) * norm.cdf(-self.d2(), 0, 1)

        return rho_result * 0.01

    def theta(self):
        """Return theta level of the Option"""
        if self.way == 'c':
            theta_result = - self.S * norm.pdf(self.d1(), 0, 1) * self.sigma / ( 2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T)* norm.cdf(self.d2(), 0, 1)

        elif self.way == 'p':
            theta_result = - self.S * norm.pdf(self.d1(), 0, 1) * self.sigma / ( 2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T)* norm.cdf(-self.d2(), 0, 1)
        
        return theta_result / 365
        
    def compute_all(self):
        return f"value: {self.value()}, delta: {self.delta()}, gamma: {self.gamma()}, vega: {self.vega()}, rho: {self.rho()}, theta: {self.theta()}"

    def implied_vol(self):
        # apply bisection method to get the implied volatility by solving the BSM function
        precision = 0.00001
        upper_vol = 500.0
        max_vol = 500.0
        min_vol = 0.0001
        lower_vol = 0.0001
        iteration = 5000
        prix_option = self.value()

        while iteration > 0:
            iteration -= 1
            mid_vol = (upper_vol + lower_vol) / 2
            price = BlackScholes(way=self.way, sigma=mid_vol, S=self.S, K=self.K, r=self.r, T=self.T, q=self.q).value()
            if self.way == 'c':
                lower_price = BlackScholes(way=self.way, sigma=lower_vol, S=self.S, K=self.K, r=self.r, T=self.T, q=self.q).value()
                if (lower_price - self.value()) * (price - self.value()) > 0:
                    lower_vol = mid_vol
                else:
                    upper_vol = mid_vol
                if mid_vol > max_vol - 5:
                    return 0.000001

            if self.way == 'p':
                upper_price = BlackScholes(way=self.way, sigma=upper_vol, S=self.S, K=self.K, r=self.r, T=self.T, q=self.q).value()
                if (upper_price - float(prix_option)) * (price - float(prix_option)) > 0:
                    upper_vol = mid_vol
                else:
                    lower_vol = mid_vol
                
                if abs(price - float(prix_option)) < precision:
                    break
            
            return mid_vol
        
    
    def plot(self, variable_choice):
        
        if variable_choice == 'K':
            x = np.arange(self.K * 0.5 , self.K * 1.5)
            vals_call = [BlackScholes(way='c', S=self.S, K=x, r=self.r, sigma=self.sigma, T=self.T).value() for x in x]
            vals_put = [BlackScholes(way='p', S=self.S, K=x, r=self.r, sigma=self.sigma, T=self.T).value() for x in x]
        if variable_choice == 'S':
            x = np.arange(self.S * 0.5 , self.S * 1.5)
            vals_call = [BlackScholes(way='c', S=x, K=self.K, r=self.r, sigma=self.sigma, T=self.T).value() for x in x]
            vals_put = [BlackScholes(way='p', S=x, K=self.K, r=self.r, sigma=self.sigma, T=self.T).value() for x in x]

        if variable_choice == 'r':
            x = np.arange(0.01, 0.25, 0.001)
            vals_call = [BlackScholes(way='c', S=self.S, K=self.K, r=x, sigma=self.sigma, T=self.T).value() for x in x]
            vals_put = [BlackScholes(way='p', S=self.S, K=self.K, r=x, sigma=self.sigma, T=self.T).value() for x in x]

        if variable_choice == 'sigma':
            x = np.arange(0.01, 0.25)
            vals_call = [BlackScholes(way='c', S=self.S, K=self.K, r=self.r, sigma=x, T=self.T).value() for x in x]
            vals_put = [BlackScholes(way='p', S=self.S, K=self.K, r=self.r, sigma=x, T=self.T).value() for x in x]

        if variable_choice == 'T':
            x = np.arange(self.T * 0.5 , self.T * 1.5)
            vals_call = [BlackScholes(way='c', S=self.S, K=self.K, r=self.r, sigma=self.sigma, T=x).value() for x in x]
            vals_put = [BlackScholes(way='p', S=self.S, K=self.K, r=self.r, sigma=self.sigma, T=x).value() for x in x]
          
        plt.plot(x, vals_call, label='Call Value')
        plt.plot(x, vals_put, label='Put Value')
        plt.axvline(self.K, color='grey', linestyle='--')
        plt.ylabel("Stock Price ($)")
        plt.xlabel("Option Price ($)")
        plt.legend()