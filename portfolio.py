import numpy as np
from typing import Optional
from pydantic import BaseModel
from yahooquery import Ticker
from typing import Dict, List
from stock import Stock


class Portfolio(BaseModel):
    name: str
    underlyings: List = []