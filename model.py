from pydantic import BaseModel, Field
from uuid import uuid4, UUID
import numpy as np
from scipy.stats import norm
from typing import Optional
from enum import Enum
from datetime import datetime



class BlackScholesModel(BaseModel):
    spot: float
    r: float
    sigma: float
    id_: UUID = Field(default_factory=uuid4)

    def pricer_vanilla(self, t, way, k, qty):

        d1 = (np.log(self.spot / k) + (self.r + self.sigma ** 2 / 2) * t) / (self.sigma * np.sqrt(t))
        d2 = d1 - (self.sigma * np.sqrt(t))
        if way == "call":
            value = self.spot * norm.cdf(d1) - k * np.exp(-self.r * t) * norm.cdf(d2)
            delta = np.exp(-self.r * t) * norm.cdf(d1) * qty
            rho = k * t * np.exp(-self.r * t) * norm.pdf(d2)
            theta = qty * - self.spot * norm.pdf(d1) * self.sigma / ( 2 * np.sqrt(t)) - self.r * k * np.exp(-self.r * t)* norm.cdf(d2)

        elif way == "put":
            value = k * np.exp(-self.r * t) * norm.cdf(-d2) - self.spot * norm.cdf(-d1)
            delta = np.exp(-self.r * t) * (norm.cdf(d1) - 1) * qty
            rho = qty * -k * t * np.exp(-self.r * t) * norm.pdf(-d2)
            theta = qty * - self.spot * norm.pdf(d1) * self.sigma / ( 2 * np.sqrt(t)) + self.r * k * np.exp(-self.r * t)* norm.cdf(-d2) / 365
        
        gamma = norm.pdf(d1) / (self.spot * self.sigma * np.sqrt(t)) * qty
        vega = self.spot * np.sqrt(t) * norm.pdf(d1) * 0.01 * qty

        return {
            "spot": self.spot,
            "r": self.r,
            "q": qty,
            "sigma": self.sigma,
            "strike": k,
            "maturity": t,
            "value": value,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def pricer_asian(self, t, way, k, b):
        sigma_a = self.sigma / np.sqrt(3)
        b_a = 1 / 2 * (b - (self.sigma ** 2 / 6))
        d1 = (np.log(self.spot / k) + (b_a + sigma_a ** 2 / 2) * t) / (sigma_a * np.sqrt(t))
        d2 = d1 - (sigma_a * np.sqrt(t))
    
        if way =="call":
            price = self.spot * np.exp((b_a - self.r) * t) * norm.cdf(d1) - k * np.exp(-self.r * t) * norm.cdf(d2)
            return price
        if way == "put":
            price = k * np.exp(-self.r * t) * norm.cdf(-d2) - self.spot * np.exp((b_a - self.r) * t) * norm.cdf(-d1) 
            return price



    
    def pricer_binary(self, t, way, k):
        d1 = (np.log(self.spot / k) + (self.r + self.sigma ** 2 / 2) * t) / (self.sigma * np.sqrt(t))
        d2 = d1 - (self.sigma * np.sqrt(t))
        if way == "call_cash_or_nothing":
            return {"price": np.exp(-self.r * t) * norm.cdf(d2)}
        
        elif way == "put_cash_or_nothing":
            return {"price": np.exp(-self.r * t) * norm.cdf(-d2)}
        
        elif way == "call_asset_or_nothing":
            return {"price": self.spot * np.exp(-self.q * t) * norm.cdf(d1)}
        
        elif way == "put_asset_or_nothing":
            return {"price": self.spot * np.exp(-self.q * t) * norm.cdf(-d1)}


class MonteCarloSimulation(BaseModel):
    spot: float
    r: float
    sigma: float
    iterations: int = 10000
    id_: UUID = Field(default_factory=uuid4)

    def pricer_vanilla(self, t, way, k):
        if way == "call":
            option_data = np.zeros([self.iterations, 2])
            rand = np.random.normal(0,1, [1, self.iterations])
            stock_price = self.spot * np.exp(t * (self.r - 0.5* self.sigma ** 2) + self.sigma * np.sqrt(t) * rand)
            option_data[:,1] = stock_price - k

            # average for the Monte Carlo Method
            average = np.sum(np.amax(option_data, axis = 1))/float(self.iterations)

            return np.exp(-1.0 * self.r * t) * average


        elif way == "put":
            option_data = np.zeros([self.iterations,2])
            rand = np.random.normal(0,1,[1,self.iterations])
            stock_price = self.spot * np.exp(t * (self.r - 0.5 * self.sigma ** 2) + self.sigma * np.sqrt(t) * rand)
            option_data[:,1] = k - stock_price

            # average for the Monte Carlo Method
            average = np.sum(np.amax(option_data, axis = 1))/float(self.iterations)

            return np.exp(-1.0 * self.r * t) * average