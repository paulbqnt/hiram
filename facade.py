from pydantic import BaseModel
from typing import Optional
import numpy as np
from scipy.stats import norm
import abc


##########################################################################################

class OptionFacade(object, metaclass=abc.ABCMeta):
    
    def __init__(self, option, engine, data):
        self.option = option
        self.engine = engine
        self.data = data
    
    def price(self):
        return self.engine.calculate(self.option, self.data)

##########################################################################################

class PricingEngine(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def calculate(self):
        pass

class BlackScholesPricingEngine(PricingEngine):
    def __init__(self, payoff_type, pricer):
        self.__payoff_type = payoff_type
        self.__pricer = pricer
        
    @property
    def payoff_type(self):
        return self.__payoff_type

    def calculate(self, option, data):
        return self.__pricer(self, option, data)
        
    
    
def BlackScholesPricer(pricing_engine, option, data):
    strike = option.strike
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (volatility * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry)
    

    if pricing_engine.payoff_type == "call":
        price = (spot * np.exp(-dividend * expiry) * norm.cdf(d1)) - (strike * np.exp(-rate * expiry) * norm.cdf(d2))
        delta = np.exp(-rate * expiry) * norm.cdf(d1)
        rho = strike * expiry * np.exp(-rate * expiry) * norm.pdf(d2)
        theta = - spot * norm.pdf(d1) * volatility / ( 2 * np.sqrt(expiry)) - rate * strike * np.exp(-rate * expiry)* norm.cdf(d2)
        
    elif pricing_engine.payoff_type == "put":
        price = (strike * np.exp(-rate * expiry) * norm.cdf(-d2)) - (spot * np.exp(-dividend * expiry) * norm.cdf(-d1))
    else:
        raise ValueError("You must pass either a call or a put option.")
    return {
        "price": price,
        "delta": delta,
        "rho": rho,
        "theta": theta
    }

##########################################################################################

class Payoff(object, metaclass=abc.ABCMeta):
    pass


class VanillaPayoff(BaseModel, Payoff):
    expiry: float
    strike: float
    payoff: str
    
    def call_payoff(self, option, spot):
        return max(spot - self.strike, 0.0)
    
    def put_payoff(self, option, spot):
        return max(option.strike - spot, 0.0)
    


##########################################################################################

class MarketData(BaseModel):
    spot: float
    rate: float
    volatility: float
    dividend: Optional[float] = 0
    
    def get_data(self):
        return (self.spot, self.rate, self.volatility, self.dividend)

##########################################################################################
data = MarketData(rate=0.05, spot=100, volatility=0.25)
call = VanillaPayoff(expiry=1, strike=100, payoff="call")
bs_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
bs_option = OptionFacade(call, bs_engine, data)
print(bs_option.data.spot)

