from pydantic import BaseModel, Field
import numpy as np
from stock import Stock
from scipy.stats import norm
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID



class VanillaOption(BaseModel):
    way: str
    k: float
    t: float
    qty: float = 1
    price: float = 1
    q: float = 0
    style: str
    stock: Optional[Stock] = None
    id_: UUID = Field(default_factory=uuid4)
    pricing_data: dict = {}


    def pricer(self, model):
        if self.style == "euro":
            self.pricing_data = model.pricer_vanilla(self.t, self.way, self.k, self.qty)
            return model.pricer_vanilla(self.t, self.way, self.k, self.qty)
        else:
            raise ValueError("Invalid style")

class AsianOption(VanillaOption):
    b: float
    def pricer(self, model):
        if self.style == "euro":
            self.pricing_data = model.pricer_asian(self.t, self.way, self.k, self.b)
            return model.pricer_asian(self.t, self.way, self.k, self.b)
        else:
            raise ValueError("Invalid style")

class ExoticOption(VanillaOption):
    def pricer(self, model):
        if self.style == "euro":
            self.pricing_data = model.pricer_binary(self.t, self.way, self.k)
            return model.pricer_binary(self.t, self.way, self.k)
        else:
            raise ValueError("Invalid style")





