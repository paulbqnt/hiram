from datetime import datetime, timedelta
from yahooquery import Ticker
import pandas as pd
from typing import Optional


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
        hist_df = Ticker(self.ticker).history(start=(datetime.today() - timedelta(days=365*5)).strftime("%Y-%m-%d"), end=datetime.today().strftime("%Y-%m-%d"))
        return hist_df
    
    def historical_volatility(self):
        pass
    
    def garman_klass_volatility(self):
        pass
    
    def parkinson_historic_volatility(self):
        pass