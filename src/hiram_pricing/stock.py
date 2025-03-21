from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd
from yfinance import Ticker


class Stock:
    def __init__(self, ticker, price: Optional[float] = None, hist: Optional[pd.DataFrame] = None, **data):
        self.ticker = ticker
        self.price = price
        self.hist = hist

        if 'ticker' in data:
            self.ticker = data['ticker']

        if 'hist' in data:
            self.hist = data['hist']

        if self.ticker is not None and self.hist is None:
            self.hist = self._fetch_history()

        if self.hist is not None and self.price is None:
            self.price = self.hist['adjclose'][-1]

    def _fetch_history(self):
        hist_df = Ticker(self.ticker).history(start=(datetime.today() - timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
                                              end=datetime.today().strftime("%Y-%m-%d"))
        return hist_df

    def historical_volatility(self, window_size=252):
        temp_df = self.hist['close'].copy()
        historical_volatility = temp_df.pct_change().rolling(window_size).std()*(252 ** 0.5)
        return historical_volatility
    def parkinson_historic_volatility(self):
        temp_df = self.hist.copy()
        temp_df['C/C'] = temp_df['close'].pct_change()
        temp_df['log^2(H/L)'] = np.log(temp_df['high'] / temp_df['low']) ** 2
        parkinson_vol = np.sqrt(temp_df['log^2(H/L)'].mean() / (4 * np.log(2)))
        return parkinson_vol

    def garman_klass_volatility(self):
        temp_df = self.hist.copy()
        temp_df['C/C'] = temp_df['close'].pct_change()
        temp_df['log^2(H/L)'] = np.log(temp_df['high'] / temp_df['low']) ** 2
        temp_df['log^2(C/O)'] = np.log(temp_df['close'] / temp_df['open']) ** 2
        temp_df['garman_klass'] = temp_df['log^2(H/L)'] * 1 / 2 + temp_df['log^2(C/O)'] * (2 * np.log(2) - 1)
        garman_klass_vol = np.sqrt(temp_df['garman_klass'].mean())
        return garman_klass_vol

    def rogers_satchel_volatility(self):
        temp_df = self.hist.copy()
        temp_df['C/C'] = temp_df['close'].pct_change()
        temp_df['norm_o'] = np.log(temp_df['open'] / temp_df['close'].shift())
        temp_df['norm_u'] = np.log(temp_df['high'] / temp_df['open'])
        temp_df['norm_d'] = np.log(temp_df['low'] / temp_df['open'])
        temp_df['norm_c'] = np.log(temp_df['close'] / temp_df['open'])

        temp_df['RS'] = (temp_df['norm_u'] * (temp_df['norm_u'] - temp_df['norm_c']) + temp_df['norm_d'] *
                         (temp_df['norm_d'] - temp_df['norm_c']))
        roger_satchell_vol = np.sqrt(temp_df['RS'].mean())
        return roger_satchell_vol

    def yang_zhang_volatility(self):
        temp_df = self.hist.copy()
        roger_satchel_vol = self.rogers_satchel_volatility()
        temp_df['C/C'] = temp_df['close'].pct_change()
        temp_df['norm_o'] = np.log(temp_df['open'] / temp_df['close'].shift())
        temp_df['norm_u'] = np.log(temp_df['high'] / temp_df['open'])
        temp_df['norm_d'] = np.log(temp_df['low'] / temp_df['open'])
        temp_df['norm_c'] = np.log(temp_df['close'] / temp_df['open'])
        std_norm_o = temp_df['norm_o'].std()
        std_norm_c = temp_df['norm_c'].std()
        k = 0.34 / (1.34 + ((temp_df.shape[0] + 1) / (temp_df.shape[0] - 1)))
        yang_zhang_vol = np.sqrt(std_norm_o ** 2 + k * std_norm_c ** 2 + (1 - k) * roger_satchel_vol ** 2)
        return yang_zhang_vol

    def sharpe_ratio(self):
        pass
