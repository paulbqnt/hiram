from facade import OptionFacade
from market_data import MarketData
from payoff import VanillaPayoff, call_payoff
from engine import MonteCarloPricingEngine, MonteCarloPricerVanilla


if __name__ == "__main__":
    call = VanillaPayoff(1, 100, call_payoff)
    market_data = MarketData(100, 0.06, 0.2, 0)
    mc_engine = MonteCarloPricingEngine(1000000, MonteCarloPricerVanilla)
    facade = OptionFacade(call, mc_engine, market_data)
    print(facade.price())

