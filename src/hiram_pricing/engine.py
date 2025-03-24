import abc
import numpy as np

from src.hiram_pricing import engine_helper as eh
from payoff import CallPayoff, PutPayoff


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
    return


def AmericanBinomialPricer(pricing_engine, option, data):
    return


class BlackScholesPricingEngine(PricingEngine):
    def __init__(self, pricer):
        self.__pricer = pricer


    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def BlackScholesPricer(pricing_engine, option, data):
    strike = option.strike
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

    def calculate_delta(epsilon=0.0001):
        np.random.seed(123)
        (spot, rate, volatility, dividend) = data.get_data()
        price_up = price_option(spot=spot + epsilon, rate=rate, volatility=volatility)
        price_down = price_option(spot=spot - epsilon, rate=rate, volatility=volatility)
        delta = (price_up - price_down) / (2 * epsilon)
        return delta

    def calculate_vega(epsilon=0.0001):
        np.random.seed(123)
        (spot, rate, volatility, dividend) = data.get_data()
        price_up = price_option(spot=spot, rate=rate, volatility=volatility + epsilon)
        price_down = price_option(spot=spot, rate=rate, volatility=volatility - epsilon)

        vega = (price_up - price_down) / (2 * epsilon)
        return vega

    def calculate_rho(epsilon=0.0001):
        np.random.seed(123)
        (spot, rate, volatility, dividend) = data.get_data()
        price_up = price_option(spot=spot, rate=rate + epsilon, volatility=volatility)
        price_down = price_option(spot=spot, rate=rate - epsilon, volatility=volatility)

        rho = (price_up - price_down) / (2 * epsilon)
        return rho * 0.01

    def calculate_theta(dt=0.0001):
        np.random.seed(123)
        (spot, rate, volatility, dividend) = data.get_data()
        price_up = price_option(spot=spot, rate=rate, volatility=volatility, expiry=option.expiry + dt)
        price_down = price_option(spot=spot, rate=rate, volatility=volatility, expiry=option.expiry - dt)
        theta = (price_up - price_down) / (2 * dt)
        return theta / 365

    def calculate_gamma(epsilon=0.0001):
        np.random.seed(123)
        (spot, rate, volatility, dividend) = data.get_data()
        price_mid = price_option(spot=spot, rate=rate, volatility=volatility)
        price_up = price_option(expiry=expiry, spot=spot + epsilon, rate=rate, volatility=volatility)
        price_down = price_option(expiry=expiry, spot=spot - epsilon, rate=rate, volatility=volatility)
        gamma = (price_up - 2 * price_mid + price_down) / (epsilon ** 2)
        return gamma

    return {"value": price_option(), "delta": calculate_delta(), "vega": calculate_vega(), "gamma": calculate_gamma(),
            "theta": calculate_theta(), "rho": calculate_rho()}


def MonteCarloPricerDigital(engine, option, data):
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

    return {"value": price_option()}


def MonteCarloPricerStrategy(pricing_engine, option, data):
    np.random.seed(123)
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()

    def price_strategy(expiry=expiry, spot=spot, rate=rate, volatility=volatility, dividend=dividend):
        np.random.seed(123)
        if pricing_engine.payoff_type == "straddle":
            option_data = np.zeros([pricing_engine.iterations, 2])
            rand = np.random.normal(0, 1, [1, pricing_engine.iterations])
            stock_price = spot * np.exp(expiry * (rate - 0.5 * volatility ** 2) + volatility * np.sqrt(expiry) * rand)
            call_payoffs = np.maximum(stock_price - option.strike, 0)
            put_payoffs = np.maximum(option.strike - stock_price, 0)
            straddle_payoffs = call_payoffs + put_payoffs
            option_data[:, 1] = straddle_payoffs
            average = np.sum(np.amax(option_data, axis=1)) / float(pricing_engine.iterations)
            value = np.exp(-1.0 * rate * expiry) * average
            return value

        if pricing_engine.payoff_type == "strangle":
            np.random.seed(123)
            option_data = np.zeros([pricing_engine.iterations, 2])
            rand = np.random.normal(0, 1, [1, pricing_engine.iterations])
            stock_price = spot * np.exp(expiry * (rate - 0.5 * volatility ** 2) + volatility * np.sqrt(expiry) * rand)
            put_payoffs = np.maximum(option.strike - stock_price, 0)
            call_payoffs = np.maximum(stock_price - option.strike_2, 0)
            option_data[:, 1] = put_payoffs + call_payoffs
            average = np.sum(option_data[:, 1]) / float(pricing_engine.iterations)
            value = np.exp(-1.0 * rate * expiry) * average
            return value
        else:
            raise ValueError("You must pass either a call or a put option.")
        return value

    return price_strategy()


def MonteCarloPricerBarrier(pricing_engine, option, data):
    np.random.seed(123)
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    discount_rate = np.exp(-rate * expiry)
