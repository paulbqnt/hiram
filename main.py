from src.hiram_pricing.market_data import MarketData
from src.hiram_pricing.payoff import (
    CallPayoff,
    PutPayoff,
    BarrierDecorator,
    CompositePayoff
)
from src.hiram_pricing.option import VanillaOption, Option
from src.hiram_pricing.engine import (
    BlackScholesPricingEngine,
    BlackScholesPricer,
    MonteCarloPricingEngine,
    MonteCarloPricerVanilla,
    MonteCarloPricerBarrier
)
from src.hiram_pricing.facade import OptionFacade


# def print_option_results(result, option_type):
#     """Helper function to print option pricing results"""
#     print(f"\n{option_type} Option Results:")
#     print(f"Value: {result['value']:.4f}")
#     print(f"Delta: {result['delta']:.4f}")
#     print(f"Gamma: {result['gamma']:.4f}")
#     print(f"Vega: {result['vega']:.4f}")
#     print(f"Theta: {result['theta']:.4f}")
#     print(f"Rho: {result['rho']:.4f}")


def main():
    # Market data setup
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

    # # 2. Barrier Option (Up-and-Out Call)
    # print("\n--- Barrier Option (Up-and-Out Call) ---")
    # barrier_payoff = BarrierDecorator(
    #     base_payoff=CallPayoff(strike=100),
    #     barrier=120,
    #     barrier_type="up-and-out"
    # )
    # barrier_option = Option(
    #     payoff=barrier_payoff,
    #     expiry=1.0
    # )
    # barrier_facade = OptionFacade(barrier_option, pricing_engine, market)
    # barrier_result = barrier_facade.price()
    # # print_option_results(barrier_result, "Up-and-Out Barrier Call")
    #
    # # 3. Straddle Strategy (Combination of Call and Put)
    # print("\n--- Straddle Strategy ---")
    # straddle = CompositePayoff()
    # straddle.add_payoff(CallPayoff(strike=100), weight=1.0)
    # straddle.add_payoff(PutPayoff(strike=100), weight=1.0)
    #
    # straddle_option = Option(
    #     payoff=straddle,
    #     expiry=1.0
    # )
    # straddle_facade = OptionFacade(straddle_option, pricing_engine, market)
    # straddle_result = straddle_facade.price()
    # # print_option_results(straddle_result, "Straddle")
    #
    # # 4. Butterfly Spread
    # print("\n--- Butterfly Spread ---")
    # butterfly = CompositePayoff()
    # butterfly.add_payoff(CallPayoff(strike=95), weight=1.0)
    # butterfly.add_payoff(CallPayoff(strike=105), weight=1.0)
    # butterfly.add_payoff(CallPayoff(strike=100), weight=-2.0)
    #
    # butterfly_option = Option(
    #     payoff=butterfly,
    #     expiry=1.0
    # )
    # butterfly_facade = OptionFacade(butterfly_option, pricing_engine, market)
    # butterfly_result = butterfly_facade.price()
    # # print_option_results(butterfly_result, "Butterfly Spread")
    #
    # # 5. Monte Carlo Pricing for Vanilla Option
    # print("\n--- Monte Carlo Pricing ---")
    # mc_engine = MonteCarloPricingEngine(
    #     iterations=10000,
    #     pricer=MonteCarloPricerVanilla
    # )
    # mc_facade = OptionFacade(call_option, mc_engine, market)
    # mc_result = mc_facade.price()
    # print("Monte Carlo Option Pricing:")
    # print(f"Value: {mc_result['value']:.4f}")
    #
    # # 6. Monte Carlo Pricing for Barrier Option
    # print("\n--- Monte Carlo Barrier Option Pricing ---")
    # mc_barrier_engine = MonteCarloPricingEngine(
    #     iterations=10000,
    #     pricer=MonteCarloPricerBarrier
    # )
    # mc_barrier_facade = OptionFacade(barrier_option, mc_barrier_engine, market)
    # mc_barrier_result = mc_barrier_facade.price()
    # print("Monte Carlo Barrier Option Pricing:")
    # print(f"Value: {mc_barrier_result['value']:.4f}")
    #
    # print("\n--- Hull - Vanilla Call/Put - Black Scholes ---")
    #
    # market = MarketData(
    #     spot=42,
    #     rate=0.1,
    #     volatility=0.2,
    #     dividend=0.01
    # )
    # call_payoff = CallPayoff(strike=40)
    # call_option = VanillaOption(
    #     payoff=call_payoff,
    #     expiry=0.5
    # )
    #
    # put_payoff = PutPayoff(strike=40)
    # put_option = VanillaOption(
    #     payoff=put_payoff,
    #     expiry=0.5
    # )
    #
    #
    # pricing_engine = BlackScholesPricingEngine(pricer=BlackScholesPricer)
    #
    # option_call_facade = OptionFacade(call_option, pricing_engine, market)
    # call_result = option_call_facade.price()
    # option_put_facade = OptionFacade(put_option, pricing_engine, market)
    # put_result = option_put_facade.price()
    #
    # # print_option_results(call_result, "Vanilla Call")
    # # print_option_results(put_result, "Vanilla Put")
    #
    # from src.hiram_pricing.option import EuropeanOption
    # from src.hiram_pricing.plot import OptionPlotter
    # market_data = MarketData(spot=100, rate=0.05, volatility=0.2, dividend=0)
    #
    # # Create option
    # call_option = EuropeanOption(payoff=CallPayoff(strike=100), expiry=1)
    #
    # # Create pricing engine
    # pricing_engine = BlackScholesPricingEngine(BlackScholesPricer)
    #
    # # Create plotter
    # plotter = OptionPlotter(call_option, market_data, pricing_engine)
    #
    # # Plot individual greek
    # plotter.plot_greeks('delta')
    #
    # # Plot all greeks
    # plotter.plot_all_greeks()


if __name__ == "__main__":
    main()