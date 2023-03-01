from datetime import datetime, timedelta
from yahooquery import Ticker
from typing import Optional
from dataclasses import dataclass

@dataclass
class Stock:
    ticker: str
    hist: Optional = None
            
    def __post_init__(self):
        if self.hist is None:
            self.hist = Ticker(self.ticker).history(start=(datetime.today() - timedelta(days = 365*5)).strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d'))