from src.hiram.market_data import MarketData
from src.hiram.payoff import CallPayoff
from src.hiram.option import VanillaOption, Option
from src.hiram.engine import (
    BlackScholesPricingEngine,
    BlackScholesPricer,
)
from src.hiram.facade import OptionFacade


def main():
    market = MarketData(
        spot=100.0,
        rate=0.05,
        volatility=0.2,
        dividend=0.01
    )


    # 1. Vanilla Call Option
    print("\n--- Vanilla Call Option ---")
    call_payoff = CallPayoff(strike=105.0)
    call_option = VanillaOption(
        payoff=call_payoff,
        expiry=1.0
    )

    pricing_engine = BlackScholesPricingEngine(pricer=BlackScholesPricer)
    option_facade = OptionFacade(call_option, pricing_engine, market)
    call_result = option_facade.price()
    print(call_result)

if __name__ == "__main__":
    main()