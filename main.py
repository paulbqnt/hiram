from market_data import MarketData
from payoff import VanillaPayoff, call_payoff
from engine import BlackScholesPricingEngine, BlackScholesPricer, MonteCarloPricingEngine, MonteCarloPricer
from facade import OptionFacade



if __name__ == "__main__":
    call = VanillaPayoff(1, 100, call_payoff)
    data = MarketData(100, 0.05, 0.2, 0)
    bs_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    mc_engine = MonteCarloPricingEngine("call", 10000000, MonteCarloPricer)
    bs_option = OptionFacade(call, bs_engine, data)
    mc_option = OptionFacade(call, mc_engine, data)

    print("BS", bs_option.price())
    print("MC", mc_option.price())

