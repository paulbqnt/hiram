import numpy as np
from typing import Optional
from pydantic import BaseModel, Field
from yahooquery import Ticker
from typing import Dict, List
from hiram.stock import Stock
from hiram.bond import Bond
from hiram.option import BlackScholes
from uuid import uuid4, UUID



class Portfolio(BaseModel):
    name: Optional[str] = None
    
    underlyings: Dict = {
        'stocks': {},
        'options': {},
        'bonds': {},
        'portfolios': {}
    }
    id_: UUID = Field(default_factory=uuid4)

    def add_underlying(self, entry):
        if isinstance(entry, BlackScholes):
            self.underlyings["options"][entry.id_] = entry

        elif isinstance(entry, Stock):
            self.underlyings["stocks"][entry.id_] = entry

        elif isinstance(entry, Bond):
            self.underlyings["bonds"][entry.id_] = entry
        
        elif isinstance(entry, Portfolio):
            self.underlyings["portfolios"][entry.id_] = entry
    
    def get_delta(self):
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += value.delta_call()   
        
        return delta_port
