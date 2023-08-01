
from abc import ABCMeta, abstractmethod


class Payoff(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def expiry(self):
        """Get the expiry date"""
        pass

    @expiry.setter
    @abstractmethod
    def expiry(self, newExpiry):
        """Set the expiry date"""
        self.__expiry = newExpiry
        pass

    @abstractmethod
    def payoff(self):
        pass


class VanillaPayoff:
    def __init__(self, expiry, strike, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff

    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry


    @property
    def strike(self):
        return self.__strike


    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike


    def payoff(self, spot):
        return self.__payoff(self, spot)

    def option_payoff(option, spot):
        match option:
            case "call":
                return max(spot - option.strike, 0.0)
            case "put":
                return max(option.strike - spot, 0.0)
            case _:
                return

    def __repr__(self):
        return f"PayOff({self.__expiry},{self.__strike},{self.__payoff})"



def call_payoff(option, spot):
    return max(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return max(option.strike - spot, 0.0)