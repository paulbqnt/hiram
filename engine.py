import abc
from abc import ABCMeta, abstractmethod
import numpy as np
from scipy.stats import norm


class PricingEngine(object, metaclass=ABCMeta):
    @abstractmethod
    def calculate(self):
        pass


class BlackScholesPricingEngine(PricingEngine):
    def __init__(self, payoff_type, pricer):
        self.__payoff_type = payoff_type
        self.__pricer = pricer

    @property
    def payoff_type(self):
        return self.__payoff_type

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def BlackScholesPricer(pricing_engine, option, data):
    strike = option.strike
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = (np.log(spot / strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (
                volatility * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry)

    gamma = norm.pdf(d1) / (spot * volatility * np.sqrt(expiry))
    vega = spot * np.sqrt(expiry) * norm.pdf(d1) * 0.01

    if pricing_engine.payoff_type == "call":
        value = (spot * np.exp(-dividend * expiry) * norm.cdf(d1)) - (strike * np.exp(-rate * expiry) * norm.cdf(d2))
        delta = np.exp(-rate * expiry) * norm.cdf(d1)
        rho = strike * expiry * np.exp(-rate * expiry) * norm.pdf(d2)  * 0.01
        theta = - (spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry)) - rate * strike * np.exp(
            -rate * expiry) * norm.cdf(d2)) * 1/365
        return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    elif pricing_engine.payoff_type == "put":
        value = (strike * np.exp(-rate * expiry) * norm.cdf(-d2)) - (spot * np.exp(-dividend * expiry) * norm.cdf(-d1))
        delta = np.exp(-rate * expiry) * (norm.cdf(d1) - 1)
        rho = -strike * expiry * np.exp(-rate * expiry) * norm.pdf(-d2)  * 0.01
        theta = - spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry)) + rate * strike * np.exp(
            -rate * expiry) * norm.cdf(-d2)  * 1/365
        return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    else:
        raise ValueError("You must pass either a call or a put option.")


class MonteCarloPricingEngine(PricingEngine):
    def __init__(self, payoff_type, iterations, pricer):
        self.__payoff_type = payoff_type
        self.__iterations = iterations
        self.__pricer = pricer

    @property
    def payoff_type(self):
        return self.__payoff_type

    @property
    def iterations(self):
        return self.__iterations

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def MonteCarloPricer(pricing_engine, option, data):
    np.random.seed(123)
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()

    def price_option(expiry=expiry, spot=spot, rate=rate, volatility=volatility, dividend=dividend):
        np.random.seed(123)
        if pricing_engine.payoff_type == "call":
            option_data = np.zeros([pricing_engine.iterations, 2])
            rand = np.random.normal(0, 1, [1, pricing_engine.iterations])
            stock_price = spot * np.exp(expiry * (rate - 0.5 * volatility ** 2) + volatility * np.sqrt(expiry) * rand)
            option_data[:, 1] = stock_price - option.strike
            average = np.sum(np.amax(option_data, axis=1)) / float(pricing_engine.iterations)
            value = np.exp(-1.0 * rate * expiry) * average
        elif pricing_engine.payoff_type == "put":
            value = None
        else:
            raise ValueError("You must pass either a call or a put option.")
        return value

    def calculate_delta(epsilon=0.0001, spot=spot):
        np.random.seed(123)
        price_up = price_option(expiry=expiry, spot=spot + epsilon, rate=rate, volatility=volatility, dividend=dividend)
        price_down = price_option(expiry=expiry, spot=spot - epsilon, rate=rate, volatility=volatility,
                                  dividend=dividend)
        delta = (price_up - price_down) / ((spot + epsilon) - (spot - epsilon))
        return delta

    def calculate_gamma(epsilon=0.0001, spot=spot):
        np.random.seed(123)
        price_mid = price_option(expiry=expiry, spot=spot, rate=rate, volatility=volatility, dividend=dividend)
        price_up = price_option(expiry=expiry, spot=spot + epsilon, rate=rate, volatility=volatility, dividend=dividend)
        price_down = price_option(expiry=expiry, spot=spot - epsilon, rate=rate, volatility=volatility,
                                  dividend=dividend)
        gamma = (price_up - 2 * price_mid + price_down) / (epsilon ** 2)
        return gamma

    def calculate_vega(epsilon=0.0001, volatility=volatility):
        np.random.seed(123)
        price_up = price_option(expiry=expiry, spot=spot, rate=rate, volatility=volatility + epsilon, dividend=dividend)
        price_down = price_option(expiry=expiry, spot=spot, rate=rate, volatility=volatility - epsilon,
                                  dividend=dividend)
        vega = (price_up - price_down) / (2 * epsilon)
        return vega * 0.01

    def calculate_theta(epsilon=0.0001, expiry=expiry):
        np.random.seed(123)
        price_up = price_option(expiry=expiry + epsilon, spot=spot, rate=rate, volatility=volatility, dividend=dividend)
        price_down = price_option(expiry=expiry - epsilon, spot=spot, rate=rate, volatility=volatility,
                                  dividend=dividend)
        theta = - (price_up - price_down) / (2 * epsilon) * 1/365
        return theta

    def calculate_rho(epsilon=0.0000001, rate=rate):
        np.random.seed(123)
        price_up = price_option(expiry=expiry, spot=spot, rate=rate + epsilon, volatility=volatility, dividend=dividend)
        price_down = price_option(expiry=expiry, spot=spot, rate=rate - epsilon, volatility=volatility,
                                  dividend=dividend)
        rho = (price_up - price_down) / (2 * epsilon)
        return rho * 0.01

    return {"value": price_option(),
            "delta": calculate_delta(),
            "gamma": calculate_gamma(),
            "vega": calculate_vega(),
            "theta": calculate_theta(),
            "rho": calculate_rho()}
