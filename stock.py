from datetime import datetime, timedelta
from yahooquery import Ticker
import pandas as pd
from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import uuid4, UUID
from enum import Enum

class Stock:
    def __init__(self, ticker: str = None, price: Optional[float] = None, hist: Optional[pd.DataFrame] = None):
        self.__ticker = ticker,
        self.__price = price,
        self.__hist = hist

    @property
    def ticker(self):
        return self.__ticker

    @property
    def price(self):
        return self.__price

    @property
    def hist(self):
        return self.__hist

    @hist.setter
    def hist(self, new_hist):
        self.__strike = new_hist