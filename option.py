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





    # def price_exotic(self, t, way, k, h, k2):

        # if way == "put_gap":
        #     if  self.spot > k2:
        #         d1 = (np.log(self.spot / k2) + (self.r - self.q + self.sigma ** 2 / 2) * t) / (self.sigma * np.sqrt(t))
        #         d2 = d1 - self.sigma * np.sqrt(t)
        #         price = k * np.exp(-self.r  * t) * norm.cdf(-d2) - self.spot * np.exp(-self.q * t) * norm.cdf(-d1)
        #         return price

    #     if way == "call_down_in":
    #         if h <= k:
    #             lmbda = self.r - self.q + self.sigma ** 2 / self.sigma ** 2
    #             y = ((np.log(h ** 2 /(self.spot * k))) / (self.sigma * np.sqrt(t))) + lmbda * self.sigma * np.sqrt(t)
    #             price = self.spot * np.exp(-self.q * t) * (h / self.spot) * np.exp(2 * lmbda) * norm.cdf(y) - k * \
    #                 np.exp(-self.r * t) * (h / self.spot) * np.exp(2 * lmbda - 2) * norm.cdf(y - self.sigma * np.sqrt(t))
    #             return price
                
    #     if way == "call_down_out":
    #         if h == k:
    #             x1 = ((np.log(self.spot / h) / (self.sigma * np.sqrt(t)))) + lmbda * self.sigma * np.sqrt(t)
    #             y1 = ((np.log( h / self.spot)) / (self.sigma * np.sqrt(t))) + lmbda * self.sigma * np.sqrt(t)
    #             price = self.spot * norm.cdf(x1) * np.exp(-self.q * t) - k * np.exp(-self.r * t) * \
    #                 norm.cdf(x1 - self.sigma * np.sqrt(t)) - self.spot * np.exp(-self.q * t) * (h / self.spot) * np.exp(2 * lmbda) * norm.cdf(y1) + \
    #                 k * np.exp(-self.r * t) * (h / self.spot) * np.exp(2* lmbda - 2) * norm.cdf(y1 - self.sigma * np.sqrt(t))
    #             return price
            
    #     # if h == k -> call_down_in = c - call_down_out 


                
    #     if way == "call_up_out":
    #         if h <= k:
    #             return 0
        
    #     if way == "call_up_in":
    #         if  h > k:
    #             lmbda = self.r - self.q + self.sigma ** 2 / self.sigma ** 2
    #             y = ((np.log(h ** 2 /(self.spot * k))) / (self.sigma * np.sqrt(t))) + lmbda * self.sigma * np.sqrt(t)
    #             y1 = ((np.log( h / self.spot)) / (self.sigma * np.sqrt(t))) + lmbda * self.sigma * np.sqrt(t)
    #             x1 = ((np.log(self.spot / h) / (self.sigma * np.sqrt(t)))) + lmbda * self.sigma * np.sqrt(t)
    #             price = self.spot * norm.cdf(x1) * np.exp(-self.q * t) - k * np.exp(-self.r * t) * norm.cdf(x1 - self.sigma * np.sqrt(t)) - \
    #                 self.spot * np.exp(-self.q * t) * (h / self.spot) * np.exp(2 * lmbda) * (norm.cdf(-y) - norm.cdf(-y1)) + \
    #                 k * np.exp(-self.r * t) * (h / self.spot) * np.exp(2 * lmbda - 2) * (norm.cdf(-y + self.sigma * np.sqrt(t) - norm.cdf(-y1 + self.sigma * np.sqrt(t))))
            
    #     # if h > k -> call_up_out = (c - call_up_in)

    #     # PUT TO ADD
                






    