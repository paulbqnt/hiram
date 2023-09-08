import numpy as np
from scipy.stats import norm
import abc


class PricingEngine(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
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
            -rate * expiry) * norm.cdf(-d2) * 1/365
        return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    elif pricing_engine.payoff_type == "straddle":
        gamma = norm.pdf(d1) / (spot * volatility * np.sqrt(expiry))
        vega = spot * np.sqrt(expiry) * norm.pdf(d1) * 0.01
        value_call = (spot * np.exp(-dividend * expiry) * norm.cdf(d1)) - (strike * np.exp(-rate * expiry) * norm.cdf(d2))
        value_put = (strike * np.exp(-rate * expiry) * norm.cdf(-d2)) - (spot * np.exp(-dividend * expiry) * norm.cdf(-d1))

        delta_call = np.exp(-rate * expiry) * norm.cdf(d1)
        delta_put = np.exp(-rate * expiry) * (norm.cdf(d1) - 1)
        rho_call = strike * expiry * np.exp(-rate * expiry) * norm.pdf(d2)  * 0.01
        rho_put = -strike * expiry * np.exp(-rate * expiry) * norm.pdf(-d2)  * 0.01
        theta_call = - (spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry)) - rate * strike * np.exp(
            -rate * expiry) * norm.cdf(d2)) * 1/365
        theta_put = - spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry)) + rate * strike * np.exp(
            -rate * expiry) * norm.cdf(-d2) * 1/365

        return {"value": (value_call+value_put), "delta": (delta_call+delta_put), "gamma": (gamma * 2), "vega": (vega * 2), "theta": (theta_call+theta_put), "rho": (rho_call+rho_put)}

    else:
        raise ValueError("You must pass either a call or a put option.")


class MonteCarloPricingEngine(PricingEngine):
    def __init__(self, iterations, pricer):
        self.__iterations = iterations
        self.__pricer = pricer

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
        price_up = price_option(spot=spot+epsilon, rate=rate, volatility=volatility)
        price_down = price_option(spot=spot-epsilon, rate=rate, volatility=volatility)
        delta = (price_up - price_down) / (2 * epsilon)
        return delta

    def calculate_vega(epsilon=0.0001):
        np.random.seed(123)
        (spot, rate, volatility, dividend) = data.get_data()
        price_up = price_option(spot=spot, rate=rate, volatility=volatility+epsilon)
        price_down = price_option(spot=spot, rate=rate, volatility=volatility-epsilon)

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
        price_up = price_option(spot=spot, rate=rate, volatility=volatility, expiry=option.expiry+dt)
        price_down = price_option(spot=spot, rate=rate, volatility=volatility,expiry=option.expiry-dt)
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

    return {"value": price_option(), "delta": calculate_delta(), "vega": calculate_vega(), "gamma": calculate_gamma(), "theta": calculate_theta(), "rho": calculate_rho()}


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

class ExoticPricingEngine(PricingEngine):
    def __init__(self, payoff_type, pricer):
        self.__payoff_type = payoff_type
        self.__pricer = pricer

    @property
    def payoff_type(self):
        return self.__payoff_type

    def calculate(self, option, data):
        return self.__pricer(self, option, data)

def StandardBarrierPricer(pricing_engine, option, data):
    np.random.seed(123)
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    pass

def BlackScholesPricerExotic(pricing_engine, option, data):
    strike = option.strike
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = (np.log(spot / strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (
                volatility * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry)