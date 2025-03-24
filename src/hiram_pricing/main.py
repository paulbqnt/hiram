from market_data import MarketData
from payoff import CallPayoff
from option import VanillaOption
from engine import BlackScholesPricingEngine, BlackScholesPricer
from facade import OptionFacade

market = MarketData(
    spot=100.0,
    rate=0.05,
    volatility=0.2,
    dividend=0.01
)

payoff = CallPayoff(strike=105.0)

option = VanillaOption(
    payoff=payoff,
    expiry=1.0
)

pricing_engine = BlackScholesPricingEngine(pricer=BlackScholesPricer)

option_facade = OptionFacade(option, pricing_engine, market)

result = option_facade.price()








print(f"Option value: {result['value']}")
print(f"Delta: {result['delta']}")
print(f"Gamma: {result['gamma']}")
print(f"Vega: {result['vega']}")
print(f"Theta: {result['theta']}")
print(f"Rho: {result['rho']}")
