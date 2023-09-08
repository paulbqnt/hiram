from facade import OptionFacade
from market_data import MarketData
from old_payoff import VanillaPayoff, call_payoff
from engine import MonteCarloPricingEngine, MonteCarloPricerVanilla, BlackScholesPricingEngine, BlackScholesPricer
from plot import Plot, plot_payoff_straddle

if __name__ == "__main__":

    # Black Scholes example
    data = MarketData(spot=45, rate=0.05, volatility=.35, dividend=0)
    call = VanillaPayoff(expiry=.25, strike=40.0, payoff=call_payoff)
    BS_engine = BlackScholesPricingEngine("straddle", BlackScholesPricer)
    BS_straddle = OptionFacade(call, BS_engine, data)

    test_plot = plot_payoff_straddle(BS_straddle)
    print(test_plot)




