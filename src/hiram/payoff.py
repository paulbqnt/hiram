from abc import ABC, abstractmethod
import numpy as np


class Payoff(ABC):
    @abstractmethod
    def __call__(self, spot_price):
        """Calculate payoff given spot price"""
        pass


class CallPayoff(Payoff):
    def __init__(self, strike):
        self.strike = strike

    def __call__(self, spot_price):
        return np.maximum(spot_price - self.strike, 0)


class PutPayoff(Payoff):
    def __init__(self, strike):
        self.strike = strike

    def __call__(self, spot_price):
        return np.maximum(self.strike - spot_price, 0)
