import unittest
import numpy as np

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
    MonteCarloPricerVanilla
)
from src.hiram_pricing.facade import OptionFacade


class TestOptionPricing(unittest.TestCase):
    def setUp(self):
        """
        Set up common market data and pricing engine for tests
        """
        self.market = MarketData(
            spot=100.0,
            rate=0.05,
            volatility=0.2,
            dividend=0.01
        )
        self.pricing_engine = BlackScholesPricingEngine(pricer=BlackScholesPricer)



    def test_barrier_up_and_out_option(self):
        """
        Test pricing of an up-and-out barrier option
        """
        barrier_payoff = BarrierDecorator(
            base_payoff=CallPayoff(strike=100),
            barrier=120,
            barrier_type="up-and-out"
        )
        barrier_option = Option(
            payoff=barrier_payoff,
            expiry=1.0
        )

        option_facade = OptionFacade(barrier_option, self.pricing_engine, self.market)
        result = option_facade.price()

        # Basic validation of results
        self.assertIsNotNone(result['value'])
        self.assertTrue(result['value'] >= 0)
        self.assertTrue(0 <= result['delta'] <= 1)

    def test_straddle_strategy(self):
        """
        Test pricing of a straddle strategy (buying both call and put)
        """
        straddle = CompositePayoff()
        straddle.add_payoff(CallPayoff(strike=100), weight=1.0)
        straddle.add_payoff(PutPayoff(strike=100), weight=1.0)

        straddle_option = Option(
            payoff=straddle,
            expiry=1.0
        )

        option_facade = OptionFacade(straddle_option, self.pricing_engine, self.market)
        result = option_facade.price()

        # Basic validation of results
        self.assertIsNotNone(result['value'])
        self.assertTrue(result['value'] > 0)

    def test_butterfly_spread(self):
        """
        Test pricing of a butterfly spread
        """
        butterfly = CompositePayoff()
        butterfly.add_payoff(CallPayoff(strike=95), weight=1.0)
        butterfly.add_payoff(CallPayoff(strike=105), weight=1.0)
        butterfly.add_payoff(CallPayoff(strike=100), weight=-2.0)

        butterfly_option = Option(
            payoff=butterfly,
            expiry=1.0
        )

        option_facade = OptionFacade(butterfly_option, self.pricing_engine, self.market)
        result = option_facade.price()

        # Basic validation of results
        self.assertIsNotNone(result['value'])
        self.assertTrue(result['value'] >= 0)

    def test_monte_carlo_vanilla_option(self):
        """
        Test Monte Carlo pricing for a vanilla option
        """
        call_payoff = CallPayoff(strike=105.0)
        call_option = VanillaOption(
            payoff=call_payoff,
            expiry=1.0
        )

        mc_engine = MonteCarloPricingEngine(
            iterations=10000,
            pricer=MonteCarloPricerVanilla
        )

        option_facade = OptionFacade(call_option, mc_engine, self.market)
        result = option_facade.price()

        # Basic validation of Monte Carlo results
        self.assertIsNotNone(result['value'])
        self.assertTrue(result['value'] > 0)

    def test_payoff_calculations(self):
        """
        Test individual payoff calculations
        """
        # Call payoff
        call_payoff = CallPayoff(strike=100)
        spot_prices = np.array([90, 100, 110])
        expected_call_payoffs = np.array([0, 0, 10])
        np.testing.assert_array_almost_equal(
            call_payoff(spot_prices),
            expected_call_payoffs
        )

        # Put payoff
        put_payoff = PutPayoff(strike=100)
        expected_put_payoffs = np.array([10, 0, 0])
        np.testing.assert_array_almost_equal(
            put_payoff(spot_prices),
            expected_put_payoffs
        )

    def test_composite_payoff(self):
        """
        Test composite payoff calculations
        """
        composite = CompositePayoff()
        call_payoff = CallPayoff(strike=100)
        put_payoff = PutPayoff(strike=100)

        composite.add_payoff(call_payoff, weight=1.0)
        composite.add_payoff(put_payoff, weight=1.0)

        spot_prices = np.array([90, 100, 110])

        # Expected payoffs:
        # At 90: 0 (call) + 10 (put) = 10
        # At 100: 0 (call) + 0 (put) = 0
        # At 110: 10 (call) + 0 (put) = 10
        expected_composite_payoffs = np.array([10, 0, 10])

        np.testing.assert_array_almost_equal(
            composite(spot_prices),
            expected_composite_payoffs
        )


def main():
    unittest.main()


if __name__ == '__main__':
    main()