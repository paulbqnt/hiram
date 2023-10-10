from old_payoff import VanillaPayoff, call_payoff, put_payoff

from hiram.engine import BlackScholesPricingEngine, BlackScholesPricer
from hiram.facade import OptionFacade
from market_data import MarketData


class Strategy:

    def __init__(self, option, engine, data):
        self.option = option
        self.engine = engine
        self.data = data

    def price(self):
        return self.engine.calculate(self.option, self.data)


call = VanillaPayoff(1, 100, call_payoff)
put = VanillaPayoff(1, 100, put_payoff())
data = MarketData(100, 0.05, 0.2, 0)
bs_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
bs_option = OptionFacade(call, bs_engine, data)

def pricer_straddle(option, engine, data):
    bs_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
