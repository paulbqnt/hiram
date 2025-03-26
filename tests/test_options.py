import pytest

from src.hiram_pricing.engine import BlackScholesPricingEngine, BlackScholesPricer
from src.hiram_pricing.facade import OptionFacade
from src.hiram_pricing.market_data import MarketData
from src.hiram_pricing.option import VanillaOption
from src.hiram_pricing.payoff import CallPayoff, PutPayoff

@pytest.mark.parametrize(
    "option_type, spot, rate, dividend, volatility, strike, expiry, expected_value",
    [
        ("call", 50, 0.05, 0, 0.3, 50, 1, 7.116),  # Hull Chapter 11.1
        ("put", 50, 0.05, 0, 0.3, 50, 1, 4.677),   # Hull Chapter 11.1

        ("call", 42, 0.1, 0, 0.2, 40, 0.5, 4.76),   # Hull Chapter 15.8 (ex 15.6)
        ("put", 42, 0.1, 0, 0.2, 40, 0.5, 0.81),   # Hull Chapter 15.8 (ex 15.6)

        ("call", 930, 0.08, 0.03, 0.2, 900, 2/12, 51.83),  # Hull Chapter 17.4 (ex 17.1)
        # ("put", 930, 0.08, 0.03, 0.2, 900, 2/12, 0.81),  # Hull Chapter 15.8 (ex 15.6)

    ]
)
def test_vanilla_option(option_type, spot, rate, dividend, volatility, strike, expiry, expected_value):
    market_data = MarketData(
        spot=spot,
        rate=rate,
        dividend=dividend,
        volatility=volatility
    )

    if option_type == "call":
        payoff = CallPayoff(strike=strike)
    elif option_type == "put":
        payoff = PutPayoff(strike=strike)
    else:
        raise ValueError("Invalid option type")

    option = VanillaOption(payoff=payoff, expiry=expiry)
    pricing_engine = BlackScholesPricingEngine(pricer=BlackScholesPricer)
    option_facade = OptionFacade(option, pricing_engine, data=market_data)

    assert option_facade.price().get('value') == pytest.approx(expected_value, rel=1e-3)

# TODO: add tests for the greeks