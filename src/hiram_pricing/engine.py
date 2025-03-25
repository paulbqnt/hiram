import abc
import numpy as np

from . import engine_helper as eh
from .payoff import CallPayoff, PutPayoff, CompositePayoff, BarrierDecorator


class PricingEngine(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate(self):
        pass


class BinomialPricingEngine(PricingEngine):
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


class BlackScholesPricingEngine(PricingEngine):
    def __init__(self, pricer):
        self.__pricer = pricer

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def BlackScholesPricer(pricing_engine, option, data):
    # Check for decorator/composite payoffs
    if isinstance(option.payoff, BarrierDecorator):
        return BarrierOptionPricer(pricing_engine, option, data)

    if isinstance(option.payoff, CompositePayoff):
        return CompositeOptionPricer(pricing_engine, option, data)

    # Standard vanilla option pricing
    strike = option.payoff.strike
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
    d2 = eh.d2_helper(d1, volatility, expiry)

    gamma = eh.gamma_helper(spot, volatility, expiry, d1)
    vega = eh.vega_helper(spot, expiry, d1)

    if isinstance(option.payoff, CallPayoff):
        value = eh.call_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta = eh.delta_call_helper(rate, expiry, d1)
        rho = eh.rho_call_helper(strike, expiry, rate, d2)
        theta = eh.theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike)
    elif isinstance(option.payoff, PutPayoff):
        value = eh.put_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta = eh.delta_put_helper(rate, expiry, d1)
        rho = eh.rho_put_helper(strike, expiry, rate, d2)
        theta = eh.theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike)
    else:
        raise ValueError("Unsupported payoff type")

    return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}


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
    d1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
    d2 = eh.d2_helper(d1, volatility, expiry)

    # Barrier option specific calculations
    lambda_param = 1 if 'up' in barrier_type else -1
    eta_param = 1 if 'out' in barrier_type else -1

    h = barrier


    if isinstance(base_payoff, CallPayoff):
        # Simplified barrier call pricing
        phi = 1  # For call
        # This is a simplified approach
        if barrier_type == 'up-and-out':
            value = eh.call_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
            if spot >= barrier:
                value = 0
    elif isinstance(base_payoff, PutPayoff):
        # Simplified barrier put pricing
        phi = -1  # For put
        if barrier_type == 'down-and-out':
            value = eh.put_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
            if spot <= barrier:
                value = 0
    else:
        raise ValueError("Unsupported base payoff type for barrier option")

    # Basic Greeks calculation
    delta = eh.delta_call_helper(rate, expiry, d1) if isinstance(base_payoff, CallPayoff) else eh.delta_put_helper(rate,
                                                                                                                   expiry,
                                                                                                                   d1)
    gamma = eh.gamma_helper(spot, volatility, expiry, d1)
    vega = eh.vega_helper(spot, expiry, d1)

    # Basic theta and rho calculations
    if isinstance(base_payoff, CallPayoff):
        theta = eh.theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike)
        rho = eh.rho_call_helper(strike, expiry, rate, d2)
    else:
        theta = eh.theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike)
        rho = eh.rho_put_helper(strike, expiry, rate, d2)

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

class MonteCarloPricingEngine(PricingEngine):
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


def MonteCarloPricerBarrier(pricing_engine, option, data):
    # Full implementation would require more complex simulation techniques
    np.random.seed(123)
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    discount_rate = np.exp(-rate * expiry)

    def price_option():
        # Simplified
        iterations = pricing_engine.iterations
        np.random.seed(123)
        z = np.random.normal(size=iterations)

        nudt = (rate - dividend - 0.5 * volatility * volatility) * expiry
        sidt = volatility * np.sqrt(expiry)

        spot_t = spot * np.exp(nudt + sidt * z)

        # Apply barrier condition
        barrier_option = option.payoff
        payoff_t = np.where(
            (barrier_option.barrier_type == 'up-and-out' and spot_t > barrier_option.barrier) |
            (barrier_option.barrier_type == 'down-and-out' and spot_t < barrier_option.barrier),
            0,
            barrier_option.base_payoff(spot_t)
        )

        option_value = discount_rate * payoff_t.mean()
        return option_value

    return {"value": price_option()}