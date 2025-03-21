import abc

import engine_helper as eh
import numpy as np


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
    d1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
    d2 = eh.d2_helper(d1, volatility, expiry)

    gamma = eh.gamma_helper(spot, volatility, expiry, d1)
    vega = eh.vega_helper(spot, expiry, d1)

    if pricing_engine.payoff_type == "call":
        value = eh.call_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta = eh.delta_call_helper(rate, expiry, d1)
        rho = eh.rho_call_helper(strike, expiry, rate, d2)
        theta = eh.theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike)
        return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    elif pricing_engine.payoff_type == "put":
        value = eh.put_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta = eh.delta_put_helper(rate, expiry, d1)
        rho = eh.rho_put_helper(strike, expiry, rate, d2)
        theta = eh.theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike)
        return {"value": value, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    elif pricing_engine.payoff_type == "straddle":
        value_call = eh.call_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        value_put = eh.put_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta_call = eh.delta_call_helper(rate, expiry, d1)
        delta_put = eh.delta_put_helper(rate, expiry, d1)
        rho_call = eh.rho_call_helper(strike, expiry, rate, d2)
        rho_put = eh.rho_put_helper(strike, expiry, rate, d2)
        theta_call = eh.theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike)
        theta_put = eh.theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike)
        return {"value": (value_call + value_put), "delta": (delta_call + delta_put), "gamma": (gamma * 2),
                "vega": (vega * 2), "theta": (theta_call + theta_put), "rho": (rho_call + rho_put)}

    elif pricing_engine.payoff_type == "strangle":
        strike_2 = option.strike_2
        d1_put = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
        d2_put = eh.d2_helper(d1_put, volatility, expiry)
        d1_call = eh.d1_helper(spot, strike_2, volatility, rate, dividend, expiry)
        d2_call = eh.d2_helper(d1_call, volatility, expiry)
        gamma_put = eh.gamma_helper(spot, volatility, expiry, d1_put)
        gamma_call = eh.gamma_helper(spot, volatility, expiry, d1_call)
        vega_put = eh.vega_helper(spot, expiry, d1_put)
        vega_call = eh.vega_helper(spot, expiry, d1_call)
        value_put = eh.put_value_helper(spot, strike, rate, expiry, d1_put, d2_put, dividend)
        value_call = eh.call_value_helper(spot, strike, rate, expiry, d1_call, d2_call, dividend)
        delta_put = eh.delta_put_helper(rate, expiry, d1_put)
        delta_call = eh.delta_call_helper(rate, expiry, d1_call)
        rho_put = eh.rho_call_helper(strike, expiry, rate, d2_put)
        rho_call = eh.rho_put_helper(strike, expiry, rate, d2_call)
        theta_put = eh.theta_put_helper(spot, d1_put, d2_put, volatility, expiry, rate, strike)
        theta_call = eh.theta_call_helper(spot, d1_call, d2_call, volatility, expiry, rate, strike)
        return {"value": (value_call + value_put), "delta": (delta_call + delta_put), "gamma": (gamma_call + gamma_put),
                "vega": (vega_call + vega_put), "theta": (theta_call + theta_put), "rho": (rho_call + rho_put)}

    elif pricing_engine.payoff_type == "bull_spread":
        strike_2 = option.strike_2

        # long call
        d1_option_1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
        d2_option_1 = eh.d2_helper(d1_option_1, volatility, expiry)

        # short call
        d1_option_2 = eh.d1_helper(spot, strike_2, volatility, rate, dividend, expiry)
        d2_option_2 = eh.d2_helper(d1_option_2, volatility, expiry)

        gamma_option_1 = eh.gamma_helper(spot, volatility, expiry, d1_option_1)
        gamma_option_2 = eh.gamma_helper(spot, volatility, expiry, d1_option_2)
        vega_option_1 = eh.vega_helper(spot, expiry, d1_option_1)
        vega_option_2 = eh.vega_helper(spot, expiry, d1_option_2)
        value_option_1 = eh.call_value_helper(spot, strike, rate, expiry, d1_option_1, d2_option_1, dividend)
        value_option_2 = eh.call_value_helper(spot, strike, rate, expiry, d1_option_2, d2_option_2, dividend)
        delta_option_1 = eh.delta_call_helper(rate, expiry, d1_option_1)
        delta_option_2 = eh.delta_call_helper(rate, expiry, d1_option_2)
        rho_option_1 = eh.rho_call_helper(strike, expiry, rate, d2_option_1)
        rho_option_2 = eh.rho_call_helper(strike, expiry, rate, d2_option_2)
        theta_option_1 = eh.theta_call_helper(spot, d1_option_1, d2_option_1, volatility, expiry, rate, strike)
        theta_option_2 = eh.theta_call_helper(spot, d1_option_2, d2_option_2, volatility, expiry, rate, strike)

        return {"value": (value_option_1 + value_option_2), "delta": (delta_option_1 + delta_option_2),
                "gamma": (gamma_option_1 + gamma_option_2), "vega": (vega_option_1 + vega_option_2),
                "theta": (theta_option_1 + theta_option_2), "rho": (rho_option_1 + rho_option_2)}

    elif pricing_engine.payoff_type == "bear_spread":
        strike_2 = option.strike_2

        # short put
        d1_option_1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
        d2_option_1 = eh.d2_helper(d1_option_1, volatility, expiry)

        # long put
        d1_option_2 = eh.d1_helper(spot, strike_2, volatility, rate, dividend, expiry)
        d2_option_2 = eh.d2_helper(d1_option_2, volatility, expiry)
        gamma_option_1 = eh.gamma_helper(spot, volatility, expiry, d1_option_1)
        gamma_option_2 = eh.gamma_helper(spot, volatility, expiry, d1_option_2)
        vega_option_1 = eh.vega_helper(spot, expiry, d1_option_1)
        vega_option_2 = eh.vega_helper(spot, expiry, d1_option_2)
        value_option_1 = eh.put_value_helper(spot, strike, rate, expiry, d1_option_1, d2_option_1, dividend)
        value_option_2 = eh.put_value_helper(spot, strike_2, rate, expiry, d1_option_2, d2_option_2, dividend)
        delta_option_1 = eh.delta_put_helper(rate, expiry, d1_option_1)
        delta_option_2 = eh.delta_put_helper(rate, expiry, d1_option_2)
        rho_option_1 = eh.rho_put_helper(strike, expiry, rate, d2_option_1)
        rho_option_2 = eh.rho_put_helper(strike_2, expiry, rate, d2_option_2)
        theta_option_1 = eh.theta_put_helper(spot, d1_option_1, d2_option_1, volatility, expiry, rate, strike)
        theta_option_2 = eh.theta_put_helper(spot, d1_option_2, d2_option_2, volatility, expiry, rate, strike_2)
        return {"value": (value_option_1 + value_option_2), "delta": (delta_option_1 + delta_option_2),
                "gamma": (gamma_option_1 + gamma_option_2), "vega": (vega_option_1 + vega_option_2),
                "theta": (theta_option_1 + theta_option_2), "rho": (rho_option_1 + rho_option_2)}

    elif pricing_engine.payoff_type == "butterfly_spread":
        strike_2 = option.strike_2
        strike_3 = option.strike_3

        # long call 1
        d1_option_1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
        d2_option_1 = eh.d2_helper(d1_option_1, volatility, expiry)

        # short 2 calls 2
        d1_option_2 = eh.d1_helper(spot, strike_2, volatility, rate, dividend, expiry)
        d2_option_2 = eh.d2_helper(d1_option_2, volatility, expiry)

        # long call 3
        d1_option_3 = eh.d1_helper(spot, strike_3, volatility, rate, dividend, expiry)
        d2_option_3 = eh.d2_helper(d1_option_3, volatility, expiry)

        gamma_option_1 = eh.gamma_helper(spot, volatility, expiry, d1_option_1)
        gamma_option_2 = eh.gamma_helper(spot, volatility, expiry, d1_option_2)
        gamma_option_3 = eh.gamma_helper(spot, volatility, expiry, d1_option_3)
        vega_option_1 = eh.vega_helper(spot, expiry, d1_option_1)
        vega_option_2 = eh.vega_helper(spot, expiry, d1_option_2)
        vega_option_3 = eh.vega_helper(spot, expiry, d1_option_3)
        value_option_1 = eh.call_value_helper(spot, strike, rate, expiry, d1_option_1, d2_option_1, dividend)
        value_option_2 = eh.call_value_helper(spot, strike_2, rate, expiry, d1_option_2, d2_option_2, dividend)
        value_option3 = eh.call_value_helper(spot, strike_3, rate, expiry, d1_option_3, d2_option_3, dividend)
        delta_option_1 = eh.delta_call_helper(rate, expiry, d1_option_1)
        delta_option_2 = eh.delta_call_helper(rate, expiry, d1_option_2)
        delta_option_3 = eh.delta_call_helper(rate, expiry, d1_option_3)
        rho_option_1 = eh.rho_call_helper(strike, expiry, rate, d2_option_1)
        rho_option_2 = eh.rho_call_helper(strike_2, expiry, rate, d2_option_2)
        rho_option_3 = eh.rho_call_helper(strike_3, expiry, rate, d2_option_3)
        theta_option_1 = eh.theta_call_helper(spot, d1_option_1, d2_option_1, volatility, expiry, rate, strike)
        theta_option_2 = eh.theta_call_helper(spot, d1_option_2, d2_option_2, volatility, expiry, rate, strike_2)
        theta_option_3 = eh.theta_call_helper(spot, d1_option_3, d2_option_3, volatility, expiry, rate, strike_3)
        return {"value": (value_option_1 + 2 * value_option_2 + value_option3),
                "delta": (delta_option_1 + 2 * delta_option_2 + delta_option_3),
                "gamma": (gamma_option_1 + 2 * gamma_option_2 + gamma_option_3),
                "vega": (vega_option_1 + 2 * vega_option_2 + vega_option_3),
                "theta": (theta_option_1 + 2 * theta_option_2 + theta_option_3),
                "rho": (rho_option_1 + 2 * rho_option_2 + rho_option_3)}

    elif pricing_engine.payoff_type == "strip":
        value_call = eh.call_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        value_put = eh.put_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta_call = eh.delta_call_helper(rate, expiry, d1)
        delta_put = eh.delta_put_helper(rate, expiry, d1)
        rho_call = eh.rho_call_helper(strike, expiry, rate, d2)
        rho_put = eh.rho_put_helper(strike, expiry, rate, d2)
        theta_call = eh.theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike)
        theta_put = eh.theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike)
        return {"value": (value_call + 2 * value_put), "delta": (delta_call + 2 * delta_put), "gamma": (gamma * 3),
                "vega": (vega * 3), "theta": (theta_call + 2 * theta_put), "rho": (rho_call + 2 * rho_put)}

    elif pricing_engine.payoff_type == "strap":
        value_call = eh.call_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        value_put = eh.put_value_helper(spot, strike, rate, expiry, d1, d2, dividend)
        delta_call = eh.delta_call_helper(rate, expiry, d1)
        delta_put = eh.delta_put_helper(rate, expiry, d1)
        rho_call = eh.rho_call_helper(strike, expiry, rate, d2)
        rho_put = eh.rho_put_helper(strike, expiry, rate, d2)
        theta_call = eh.theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike)
        theta_put = eh.theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike)
        return {"value": (2 * value_call + value_put), "delta": (2 * delta_call + delta_put), "gamma": (gamma * 3),
                "vega": (vega * 3), "theta": (2 * theta_call + theta_put), "rho": (2 * rho_call + rho_put)}

    elif pricing_engine.payoff_type == "calendar_spread":
        expiry_2 = option.expiry_2
        # short call
        d1_option_1 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry)
        d2_option_1 = eh.d2_helper(d1_option_1, volatility, expiry)

        # long call
        d1_option_2 = eh.d1_helper(spot, strike, volatility, rate, dividend, expiry_2)
        d2_option_2 = eh.d2_helper(d1_option_2, volatility, expiry_2)

        gamma_option_1 = eh.gamma_helper(spot, volatility, expiry, d1_option_1)
        gamma_option_2 = eh.gamma_helper(spot, volatility, expiry_2, d1_option_2)
        vega_option_1 = eh.vega_helper(spot, expiry, d1_option_1)
        vega_option_2 = eh.vega_helper(spot, expiry_2, d1_option_2)
        value_option_1 = eh.call_value_helper(spot, strike, rate, expiry, d1_option_1, d2_option_1, dividend)
        value_option_2 = eh.call_value_helper(spot, strike, rate, expiry_2, d1_option_2, d2_option_2, dividend)
        delta_option_1 = eh.delta_call_helper(rate, expiry, d1_option_1)
        delta_option_2 = eh.delta_call_helper(rate, expiry_2, d1_option_2)
        rho_option_1 = eh.rho_call_helper(strike, expiry, rate, d2_option_1)
        rho_option_2 = eh.rho_call_helper(strike, expiry_2, rate, d2_option_2)
        theta_option_1 = eh.theta_call_helper(spot, d1_option_1, d2_option_1, volatility, expiry, rate, strike)
        theta_option_2 = eh.theta_call_helper(spot, d1_option_2, d2_option_2, volatility, expiry_2, rate, strike)

        return {"value": (value_option_1 + value_option_2), "delta": (delta_option_1 + delta_option_2),
                "gamma": (gamma_option_1 + gamma_option_2), "vega": (vega_option_1 + vega_option_2),
                "theta": (theta_option_1 + theta_option_2), "rho": (rho_option_1 + rho_option_2)}

    else:
        raise ValueError("You must pass either a call/put/bull_spread/bear_spread/butterfly_spread/strip/strap/calendar_spread ")


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
