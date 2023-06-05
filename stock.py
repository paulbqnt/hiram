from datetime import datetime, timedelta
from yahooquery import Ticker
import pandas as pd
from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import uuid4, UUID
from enum import Enum

class Way_stock(str, Enum):
    long = 'long',
    short = 'short'

class Stock(BaseModel):
    way: Way_stock = Way_stock.long
    ticker: str
    price: Optional[float]= None
    quantity: Optional[float]= None
    id_: UUID = Field(default_factory=uuid4)
    hist: Optional[pd.DataFrame] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        data["hist"] = Ticker(data["ticker"]).history(start=(datetime.today() - timedelta(days=365*5)).
                                                      strftime("%Y-%m-%d"), end=datetime.today().strftime("%Y-%m-%d"))
        data["price"] = data["hist"]["adjclose"][-1]
        super().__init__(**data)

