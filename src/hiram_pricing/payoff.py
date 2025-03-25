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


class StraddlePayoff(Payoff):
    def __init__(self, strike):
        self.call_payoff = CallPayoff(strike)
        self.put_payoff = PutPayoff(strike)
        self.strike = strike

    def __call__(self, spot_price):
        return self.call_payoff(spot_price) + self.put_payoff(spot_price)


class CompositePayoff:
    def __init__(self):
        # Store payoffs as a list of tuples (payoff, weight)
        self.payoffs = []

    def add_payoff(self, payoff, weight=1.0):
        """
        Add a payoff to the composite with an optional weight

        :param payoff: The payoff to add (e.g., CallPayoff, PutPayoff)
        :param weight: Weight of the payoff (default is 1.0)
        """
        self.payoffs.append((payoff, weight))

    def __call__(self, spot_prices):
        """
        Calculate the payoff for the composite option

        :param spot_prices: Spot prices to calculate payoff
        :return: Composite payoff
        """
        total_payoff = 0
        for payoff, weight in self.payoffs:
            total_payoff += weight * payoff(spot_prices)
        return total_payoff

    @property
    def strike(self):
        """
        Return a representative strike price (useful for Greeks calculations)
        Assumes first payoff's strike if multiple payoffs exist
        """
        return self.payoffs[0][0].strike if self.payoffs else None

class PayoffDecorator(Payoff):
    def __init__(self, base_payoff):
        self.base_payoff = base_payoff


class BarrierDecorator(PayoffDecorator):
    def __init__(self, base_payoff, barrier, barrier_type="up-and-out"):
        super().__init__(base_payoff)
        self.barrier = barrier
        self.barrier_type = barrier_type

    def __call__(self, price_path):
        # Check if barrier is breached based on barrier_type
        if self.is_barrier_breached(price_path):
            if "out" in self.barrier_type:
                return 0

        else:
            if "in" in self.barrier_type:
                return 0


        return self.base_payoff(price_path[-1])

    def is_barrier_breached(self, price_path):
        if "up" in self.barrier_type:
            return any(price >= self.barrier for price in price_path)
        else:
            return any(price <= self.barrier for price in price_path)