import numpy as np
from typing import Optional
from pydantic import BaseModel, Field
from yahooquery import Ticker
from typing import Dict, List
from stock import Stock
from bond import Bond
from option import BlackScholes
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
        """Add an underlying wihhin it's correct category"""
        if isinstance(entry, BlackScholes):
            self.underlyings["options"][entry.id_] = entry

        elif isinstance(entry, Stock):
            self.underlyings["stocks"][entry.id_] = entry

        elif isinstance(entry, Bond):
            self.underlyings["bonds"][entry.id_] = entry
        
        elif isinstance(entry, Portfolio):
            self.underlyings["portfolios"][entry.id_] = entry
    
    def get_delta(self):
        """Return the delta of the Portfolio"""
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += value.delta() * (value.qty * value.price)
        
        return delta_port
    
    def get_gamma(self):
        """Return the gamma of the Portfolio"""
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += value.gamma() * (value.qty * value.price)
        
        return delta_port

    def get_vega(self):
        """Return the vega of the Portfolio"""
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += value.vega() * (value.qty * value.price)
        
        return delta_port

    def get_rho(self):
        """Return the rho of the Portfolio"""
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += value.rho() * (value.qty * value.price)
        
        return delta_port
    
    def get_theta(self):
        """Return the theta of the Portfolio"""
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += value.theta() * (value.qty * value.price)
        
        return delta_port
    
    def get_option_book_value(self):
        """Return the option book position in USD"""
        delta_port = 0
        for key, value in self.underlyings['options'].items():
            delta_port += (value.qty * value.price)
        
        return delta_port