from pydantic import BaseModel, Field
import numpy as np
from stock import Stock
from option import VanillaOption
from scipy.stats import norm
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID



class Strategy(BaseModel):
    way: str = "long"
    k: float
    k2: Optional[float] = None
    k3: Optional[float] = None
    t: float
    t2: Optional[float] = None
    qty: float = 1
    price: float = 1
    q: float = 0
    style: str
    stock: Optional[Stock] = None
    id_: UUID = Field(default_factory=uuid4)
    pricing_data: dict = {}


    def pricer(self, model):
        if self.style == "straddle":
            self.pricing_data = model.pricer_straddle(self.t, self.way, self.k, self.qty)
            return model.pricer_straddle(self.t, self.way, self.k, self.qty)
        
        if self.style == "strangle":
            self.pricing_data = model.pricer_strangle(self.t, self.way, self.k, self.k2, self.qty)
            return model.pricer_strangle(self.t, self.way, self.k, self.k2, self.qty)
        
        if self.style == "bull_spread":
            self.pricing_data = model.pricer_bull_spread(self.t, self.way, self.k, self.k2, self.qty)
            return model.pricer_bull_spread(self.t, self.way, self.k, self.k2, self.qty)        
        
        if self.style == "bear_spread":
            self.pricing_data = model.pricer_bear_spread(self.t, self.way, self.k, self.k2, self.qty)
            return model.pricer_bear_spread(self.t, self.way, self.k, self.k2, self.qty) 
                       
        if self.style == "butterfly_spread":
            self.pricing_data = model.pricer_butterfly_spread(self.t, self.way, self.k, self.k2, self.k3, self.qty)
            return model.pricer_butterfly_spread(self.t, self.way, self.k, self.k2, self.k3, self.qty)

        if self.style == "strip":
            self.pricing_data = model.pricer_strip(self.t, self.way, self.k, self.qty)
            return model.pricer_strip(self.t, self.way, self.k, self.qty)

        if self.style == "strap":
            self.pricing_data = model.pricer_strap(self.t, self.way, self.k, self.qty)
            return model.pricer_strap(self.t, self.way, self.k, self.qty)
        
        if self.style == "calendar_spread":
            self.pricing_data = model.pricer_calendar_spread(self.t, self.t2, self.way, self.k, self.qty)
            return model.pricer_calendar_spread(self.t, self.t2, self.way, self.k, self.qty)

        else:
            raise ValueError("Invalid style")