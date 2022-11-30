from scipy.stats import norm
import numpy as np
from yahooquery import Ticker

rates = {
    'USD': Ticker('^IRX').price.get('^IRX').get('regularMarketPrice')
}

class BlackScholes:
    def __init__(self, ticker, strike, maturity, volatility, dividend=0, spot=None, risk_free_rate=None):
        self.ticker = ticker
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.dividend = dividend

        self.spot = Ticker(self.ticker).price.get(self.ticker).get('regularMarketPrice')
        self.currency = Ticker(self.ticker).price.get(self.ticker).get('currency')
        self.risk_free_rate = rates.get(self.currency)



    def d1(self):
        return (np.log(self.spot / self.strike) + (self.risk_free_rate - self.dividend + self.volatility ** 2 / 2) * self.maturity) \
               / (self.volatility * np.sqrt(self.maturity))

    def d2(self):
        return self.d1() - self.volatility * np.sqrt(self.maturity)

    def _call_value(self):
        return self.spot * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(self.d1()) - \
               self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(self.d2())

    def _put_value(self):
        return self.strike * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(-self.d2()) - \
               self.spot * np.exp(-self.risk_free_rate * self.maturity) * norm.cdf(-self.d1())

    def price(self, type_='C'):
        if type_ == 'C':
            return self._call_value()
        if type_ == 'P':
            return self._put_value()
        if type_ == 'B':
            return {'call': self._call_value(), 'put': self._put_value()}
        else:
            raise ValueError('Unrecognized type')

    def call_delta(self):
        return norm.cdf(self.d1())

aapl = BlackScholes(ticker='AAPL', strike=160, maturity=1, volatility=0.3)
print(aapl.price(type_='P'))