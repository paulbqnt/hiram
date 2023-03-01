from typing import Optional
from pydantic import BaseModel
from yahooquery import Ticker
from typing import Dict


class Bond(BaseModel):
    principal: float
    interest: float
    period: str # enum



    ticker: Optional[str] = None
    yquery: Dict = Ticker(ticker)

    @property
    def currency(self):
        return Ticker(self.ticker).summary_detail.get('AAPL').get('currency')
