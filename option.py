from pydantic import BaseModel, Field
import numpy as np
from scipy.stats import norm
from typing import Optional
from enum import Enum
from uuid import uuid4, UUID
from stock import Stock


class Way_option(str, Enum):
    """Choose between call and put"""
    call = 'call',
    put = 'put'

class BlackScholes(BaseModel):
    """Black Scholes (1973)"""
    S: float
    K: float
    T: float
    r: float
    sigma: float
    way: Way_option
    stock: Optional[Stock]
    quantity: Optional[float] = 1
    price: Optional[float] = 1
    id_: UUID = Field(default_factory=uuid4)

    def d1(self) -> float:
        return (np.log(self.S / self.K) + (self.r + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def d2(self) -> float:
        return self.d1() - (self.sigma * np.sqrt(self.T))
    
    def value(self) -> float:
        if self.way == Way_option.call:
            return self.S * norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2())
        elif self.way == Way_option.put:
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1())

    def delta(self) -> float:
        if self.way == Way_option.call:
            #return norm.cdf(self.d1()) * (self.price * self.quantity)
            return np.exp(-self.r * self.T) * norm.cdf(self.d1())
        elif self.way == Way_option.put:
            #return (-norm.cdf(-self.d1())  * (self.price * self.quantity))
            return np.exp(-self.r * self.T) * (norm.cdf(self.d1()) - 1)

    def gamma(self) -> float:
        """Return gamma level of the Option"""
        return norm.pdf(self.d1()) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self) -> float:
        """Return vega level of the Option"""
        return self.S * np.sqrt(self.T) * norm.pdf(self.d1()) * 0.01

    def rho(self) -> float:
        if self.way == Way_option.call:
            rho_result = self.K * self.T * np.exp(-self.r *self.T) * norm.cdf(self.d2())

        elif self.way == Way_option.put:
            rho_result = -self.K * self.T * np.exp(-self.r *self.T) * norm.cdf(-self.d2())

        return rho_result * 0.01

    def theta(self) -> float:
        """Return theta level of the Option"""
        if self.way == Way_option.call:
            theta_result = - self.S * norm.pdf(self.d1()) * self.sigma / ( 2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T)* norm.cdf(self.d2())

        elif self.way == Way_option.put:
            theta_result = - self.S * norm.pdf(self.d1()) * self.sigma / ( 2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T)* norm.cdf(-self.d2())
        
        return theta_result / 365
        
    def compute_all(self):
        return f"value: {self.value()}, delta: {self.delta()}, gamma: {self.gamma()}, vega: {self.vega()}, rho: {self.rho()}, theta: {self.theta()}"

