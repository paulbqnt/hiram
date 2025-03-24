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


class CompositePayoff(Payoff):
    def __init__(self):
        self.payoffs = []
        self.weights = []

    def add_payoff(self, payoff, weight=1.0):
        self.payoffs.append(payoff)
        self.weights.append(weight)
        return self

    def __call__(self, spot_price):
        return sum(w * p(spot_price) for p, w in zip(self.payoffs, self.weights))