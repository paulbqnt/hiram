import abc
import numpy as np


class Payoff(object, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def expiry(self):
        """Get the expiry date"""
        pass

    @expiry.setter
    @abc.abstractmethod
    def expiry(self, newExpiry):
        """Set the expiry date"""
        self.__expiry = newExpiry
        pass


    @abc.abstractmethod
    def payoff(self):
        pass


class VanillaPayoff(Payoff):
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


class ExoticPayoff(Payoff):
    def __init__(self, expiry, strike, payoff, barrier):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        self.__barrier = barrier

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

    @property
    def barrier(self):
        return self.__barrier

    @barrier.setter
    def strike(self, new_barrier):
        self.__barrier = new_barrier


    def payoff(self, spot):
        return self.__payoff(self, spot)













def call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)

def digital_call_payoff(option, spot):
    if spot > option.strike:
        return 1
    else:
        return 0

def asian_call_option(option, spot):
    return np.maximum(np.mean(spot - option.strike), 0.0)

def asian_put_option(option, spot):
    return np.maximum(np.mean(option.strike - spot), 0.0)

