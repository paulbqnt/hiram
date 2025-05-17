import abc
from typing import Dict, Any

import numpy as np

from . import engine_helper as eh
from .pricers import OptionPricer
from .market_data import MarketData
from .models import PricingResult, Greeks
from .option import Option
from .payoff import CallPayoff, PutPayoff


class PricingEngine(object, metaclass=abc.ABCMeta):
    """Abstract base class for all pricing engines."""
    @classmethod
    def __pydantic_init_subclass__(cls):
        OptionPricer.model_rebuild()

    @abc.abstractmethod
    def calculate(self):
        """
        Calculate option price and Greeks.

        Args:
            option: The option to price
            data: Market data for pricing

        Returns:
            Dict containing pricing results
        """
        pass


class BinomialEngine(PricingEngine):
    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def EuropeanBinomialPricer(pricing_engine, option, data):
    # TODO: Implement European Binomial Tree pricing
    pass


def AmericanBinomialPricer(pricing_engine, option, data):
    # TODO: Implement American Binomial Tree pricing
    pass


class BlackScholesEngine(PricingEngine):
    """Pricing engine that uses Black-Scholes analytic formulas."""
    def __init__(self, pricer):
        self.__pricer = pricer

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def BlackScholesPricer(pricing_engine, option, data) -> PricingResult:
    """
        Standard Black-Scholes pricer for vanilla and exotic options.

        Args:
            pricing_engine: The Black-Scholes pricing engine
            option: The option to price
            data: Market data for pricing

        Returns:
            Dict containing pricing results
        """
    # Standard vanilla option pricing
    strike = option.payoff.strike
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = eh.d1(spot, strike, volatility, rate, dividend, expiry)
    d2 = eh.d2(d1, volatility, expiry)

    gamma = eh.gamma(spot, volatility, expiry, d1)
    vega = eh.vega(spot, expiry, d1)

    if isinstance(option.payoff, CallPayoff):
        value = eh.call_value(spot, strike, rate, expiry, d1, d2, dividend)
        delta = eh.delta_call(rate, expiry, d1)
        rho = eh.rho_call(strike, expiry, rate, d2)
        theta = eh.theta_call(spot, d1, d2, volatility, expiry, rate, strike)
    elif isinstance(option.payoff, PutPayoff):
        value = eh.put_value(spot, strike, rate, expiry, d1, d2, dividend)
        delta = eh.delta_put(rate, expiry, d1)
        rho = eh.rho_put(strike, expiry, rate, d2)
        theta = eh.theta_put(spot, d1, d2, volatility, expiry, rate, strike)
    else:
        raise ValueError("Unsupported payoff type")

    # return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}
    return PricingResult(
        value=value,
        greeks=Greeks(
            delta=delta,
            gamma=gamma,
            vega=vega,
            theta=theta,
            rho=rho
        )
    ).to_json()





def BarrierOptionPricer(pricing_engine, option, data):
    """
    Pricing for barrier options using Black-Scholes approach
    Supports up-and-out, down-and-out, up-and-in, down-and-in barrier options
    """
    barrier_option = option.payoff
    base_payoff = barrier_option.base_payoff
    barrier = barrier_option.barrier
    barrier_type = barrier_option.barrier_type

    (spot, rate, volatility, dividend) = data.get_data()
    strike = base_payoff.strike
    expiry = option.expiry

    # Calculate standard option parameters
    d1 = eh.d1(spot, strike, volatility, rate, dividend, expiry)
    d2 = eh.d2(d1, volatility, expiry)

    # Barrier option specific calculations
    lambda_param = 1 if 'up' in barrier_type else -1
    eta_param = 1 if 'out' in barrier_type else -1

    h = barrier


    if isinstance(base_payoff, CallPayoff):
        # Simplified barrier call pricing
        phi = 1  # For call
        # This is a simplified approach
        if barrier_type == 'up-and-out':
            value = eh.call_value(spot, strike, rate, expiry, d1, d2, dividend)
            if spot >= barrier:
                value = 0
    elif isinstance(base_payoff, PutPayoff):
        # Simplified barrier put pricing
        phi = -1  # For put
        if barrier_type == 'down-and-out':
            value = eh.put_value(spot, strike, rate, expiry, d1, d2, dividend)
            if spot <= barrier:
                value = 0
    else:
        raise ValueError("Unsupported base payoff type for barrier option")

    # Basic Greeks calculation
    delta = eh.delta_call(rate, expiry, d1) if isinstance(base_payoff, CallPayoff) else eh.delta_put_helper(rate,
                                                                                                                   expiry,
                                                                                                                   d1)
    gamma = eh.gamma(spot, volatility, expiry, d1)
    vega = eh.vega(spot, expiry, d1)

    # Basic theta and rho calculations
    if isinstance(base_payoff, CallPayoff):
        theta = eh.theta_call(spot, d1, d2, volatility, expiry, rate, strike)
        rho = eh.rho_call(strike, expiry, rate, d2)
    else:
        theta = eh.theta_put(spot, d1, d2, volatility, expiry, rate, strike)
        rho = eh.rho_put(strike, expiry, rate, d2)

    return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}


def CompositeOptionPricer(pricing_engine, option, data):
    """
    Pricing for composite options like straddles, butterflies, etc.
    """
    composite_payoff = option.payoff

    # Aggregate pricing for all payoffs in the composite
    total_value = 0
    total_delta = 0
    total_gamma = 0
    total_vega = 0
    total_theta = 0
    total_rho = 0

    for payoff, weight in composite_payoff.payoffs:
        # Create a temporary option with this payoff
        temp_option = type(option)(payoff=payoff, expiry=option.expiry)

        # Price the individual option
        result = BlackScholesPricer(pricing_engine, temp_option, data)

        # Aggregate with weights
        total_value += weight * result['value']
        total_delta += weight * result['delta']
        total_gamma += weight * result['gamma']
        total_vega += weight * result['vega']
        total_theta += weight * result['theta']
        total_rho += weight * result['rho']

    return {
        "value": total_value,
        "delta": total_delta,
        "gamma": total_gamma,
        "vega": total_vega,
        "theta": total_theta,
        "rho": total_rho
    }

class MonteCarloEngine(PricingEngine):
    def __init__(self, iterations, pricer, payoff_type=None):
        self.__iterations = iterations
        self.__pricer = pricer
        self.payoff_type = payoff_type

    @property
    def iterations(self):
        return self.__iterations

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def MonteCarloPricerVanilla(engine, option, data):
    np.random.seed(123)
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    discount_rate = np.exp(-rate * expiry)

    def price_option(spot=spot, rate=rate, volatility=volatility, expiry=expiry):
        np.random.seed(123)
        z = np.random.normal(size=engine.iterations)
        nudt = (rate - dividend - 0.5 * volatility * volatility) * expiry
        sidt = volatility * np.sqrt(expiry)

        spot_t = spot * np.exp(nudt + sidt * z)
        payoff_t = option.payoff(spot_t)
        option_value = discount_rate * payoff_t.mean()

        return option_value


    return {"value": price_option(), "delta": None, "vega": None, "gamma": None,
            "theta": None, "rho": None}


def MonteCarloPricerBarrier(
        pricing_engine: MonteCarloEngine,
        option: Option,
        data: MarketData
) -> Dict[str, Any]:
    """
    Monte Carlo pricer for barrier options.

    Args:
        pricing_engine: The Monte Carlo pricing engine
        option: The barrier option to price
        data: Market data for pricing

    Returns:
        Dict containing pricing results
    """
    np.random.seed(123)
    expiry = option.expiry
    spot, rate, volatility, dividend = data.get_data()
    discount_factor = np.exp(-rate * expiry)
    iterations = pricing_engine.iterations

    # Generate random paths
    z = np.random.normal(size=iterations)
    nudt = (rate - dividend - 0.5 * volatility * volatility) * expiry
    sidt = volatility * np.sqrt(expiry)

    # Calculate terminal stock prices
    spot_t = spot * np.exp(nudt + sidt * z)

    # Apply barrier condition
    barrier_option = option.payoff
    barrier = barrier_option.barrier
    barrier_type = barrier_option.barrier_type

    # Apply barrier conditions
    if barrier_type == 'up-and-out':
        payoff_t = np.where(spot_t > barrier, 0, barrier_option.base_payoff(spot_t))
    elif barrier_type == 'down-and-out':
        payoff_t = np.where(spot_t < barrier, 0, barrier_option.base_payoff(spot_t))
    elif barrier_type == 'up-and-in':
        payoff_t = np.where(spot_t > barrier, barrier_option.base_payoff(spot_t), 0)
    elif barrier_type == 'down-and-in':
        payoff_t = np.where(spot_t < barrier, barrier_option.base_payoff(spot_t), 0)
    else:
        raise ValueError(f"Unknown barrier type: {barrier_type}")

    option_value = discount_factor * payoff_t.mean()

    # For MC, Greeks would require additional simulations or other techniques
    return PricingResult(
        value=option_value,
        greeks=Greeks(delta=None, gamma=None, vega=None, theta=None, rho=None)
    ).to_json()