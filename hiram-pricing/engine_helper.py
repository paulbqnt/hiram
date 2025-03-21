"""
All the functions used within engine.py,
helps me to avoid manual discrepancy betweens options
"""


import numpy as np
from scipy.stats import norm


def d1_helper(spot, strike, volatility, rate, dividend, expiry):
    return (np.log(spot / strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (
            volatility * np.sqrt(expiry))


def d2_helper(d1, volatility, expiry):
    return d1 - volatility * np.sqrt(expiry)


def gamma_helper(spot, volatility, expiry, d1):
    return norm.pdf(d1) / (spot * volatility * np.sqrt(expiry))


def vega_helper(spot, expiry, d1):
    return spot * np.sqrt(expiry) * norm.pdf(d1) * 0.01


def call_value_helper(spot, strike, rate, expiry, d1, d2, dividend):
    return (spot * np.exp(-dividend * expiry) * norm.cdf(d1)) - (strike * np.exp(-rate * expiry) * norm.cdf(d2))


def put_value_helper(spot, strike, rate, expiry, d1, d2, dividend):
    return (strike * np.exp(-rate * expiry) * norm.cdf(-d2)) - (spot * np.exp(-dividend * expiry) * norm.cdf(-d1))


def delta_call_helper(rate, expiry, d1):
    return np.exp(-rate * expiry) * norm.cdf(d1)


def delta_put_helper(rate, expiry, d1):
    return np.exp(-rate * expiry) * (norm.cdf(d1) - 1)


def rho_call_helper(strike, expiry, rate, d2):
    return strike * expiry * np.exp(-rate * expiry) * norm.cdf(d2) * 0.01


def rho_put_helper(strike, expiry, rate, d2):
    return -strike * expiry * np.exp(-rate * expiry) * norm.cdf(-d2) * 0.01


def theta_call_helper(spot, d1, d2, volatility, expiry, rate, strike):
    return - (spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry)) - rate * strike * np.exp(-rate * expiry) *
              norm.cdf(d2)) * 1 / 365


def theta_put_helper(spot, d1, d2, volatility, expiry, rate, strike):
    return - spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry)) + rate * strike * np.exp(
            -rate * expiry) * norm.cdf(-d2) * 1 / 365
