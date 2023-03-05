from datetime import datetime, timedelta
from yahooquery import Ticker
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field
from uuid import uuid4, UUID


@dataclass
class Stock:
    ticker: str
    hist: bool = None
    meta_data = Dict = None
    id_: UUID = Field(default_factory=uuid4)

    def __post_init__(self):
        if self.hist is None:
            self.hist = Ticker(self.ticker).history(start=(datetime.today(
            ) - timedelta(days=365*5)).strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d'))
