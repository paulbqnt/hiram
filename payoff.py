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
    def expiry(self, new_expiry):
        """Set the expiry date"""
        self.__expiry = new_expiry
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



class StrategyPayoff(Payoff):
    def __init__(self, expiry, strike, payoff, strike_2=None, strike_3=None, expiry_2=None):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        self.__strike_2 = strike_2
        self.__strike_3 = strike_3
        self.__expiry_2 = expiry_2

    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry

    @property
    def expiry_2(self):
        return self.__expiry_2

    @expiry_2.setter
    def expiry_2(self, new_expiry):
        self.__expiry_2 = new_expiry

    @property
    def strike(self):
        return self.__strike

    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike

    def payoff(self, spot):
        return self.__payoff(self, spot)

    @property
    def strike_2(self):
        return self.__strike_2

    @strike_2.setter
    def strike_2(self, new_strike):
        self.__strike_2 = new_strike

    @property
    def strike_3(self):
        return self.__strike_3

    @strike_3.setter
    def strike_3(self, new_strike):
        self.__strike_3 = new_strike


class ExoticPayoff(Payoff):
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



def call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)


def put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)


def straddle_payoff(option, spot):
    return call_payoff(option, spot) + put_payoff(option, spot)


def strangle_payoff(option, spot):
    return (np.maximum(option.strike - spot, 0.0)) + (np.maximum(option.strike_2 - spot, 0.0))


# bull call spread by default
def bull_spread_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0) + (np.maximum(spot - option.strike_2, 0.0))


# bear put spread by default
def bear_spread_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0) + (np.maximum(option.strike_2 - spot, 0.0))


def butterfly_spread_payoff(option, spot):
    return (np.maximum(spot - option.strike, 0.0) + (2 * np.maximum(spot - option.strike_2, 0.0)) +
            (np.maximum(spot - option.strike_3, 0.0)))
