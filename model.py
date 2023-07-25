from pydantic import BaseModel, Field
from uuid import uuid4, UUID
import numpy as np
from option import VanillaOption
from scipy.stats import norm
from typing import Optional
from enum import Enum
from datetime import datetime


class MCEngine(BaseModel):
    spot: float
    r: float
    sigma: float
    simulations: Optional[int] = 1000000
    epsilon: Optional[float] = 0.001
    id_: UUID = Field(default_factory=uuid4)
    
    
    def pricer_vanilla(self, t, way, k, qty):
        np.random.seed(42)
        option_data = np.zeros([self.simulations, 2])
        rand = np.random.normal(0,1, [1, self.simulations])
        stock_price = self.spot * np.exp(t * (self.r - 0.5* self.sigma ** 2) + self.sigma * np.sqrt(t) * rand)
        option_data[:,1] = stock_price - k
        average = np.sum(np.amax(option_data, axis = 1))/float(self.simulations)
        value = np.exp(-1.0 * self.r * t) * average
        
        ###
        
        option_price = MCEngine(spot=100, r=0.05, sigma=0.2).pricer_vanilla(t=1, way="call", k=105, qty=1)       
        
        
        
        return {
            "value": value
        }
    
    
        
        
        

              
        
    

        
        
                

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
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def pricer_asian(self, t, way, k, b):
        """Geometric Average-Rate Options | Haug 1997"""
        sigma_a = self.sigma / np.sqrt(3)
        b_a = 1 / 2 * (b - (self.sigma ** 2 / 6))
        d1 = (np.log(self.spot / k) + (b_a + sigma_a ** 2 / 2) * t) / (sigma_a * np.sqrt(t))
        d2 = d1 - (sigma_a * np.sqrt(t))

        if way =="call":
            value = self.spot * np.exp((b_a - self.r) * t) * norm.cdf(d1) - k * np.exp(-self.r * t) * norm.cdf(d2)

        if way == "put":
            value = k * np.exp(-self.r * t) * norm.cdf(-d2) - self.spot * np.exp((b_a - self.r) * t) * norm.cdf(-d1)
       
        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


    def pricer_binary(self, t, way, k):
        d1 = (np.log(self.spot / k) + (self.r + self.sigma ** 2 / 2) * t) / (self.sigma * np.sqrt(t))
        d2 = d1 - (self.sigma * np.sqrt(t))
        
        if way == "call":
            value = np.exp(-self.r * t) * norm.cdf(d2)
            delta = (np.exp(-self.r * (t)) * norm.pdf(d2)) / (self.sigma * self.spot * np.sqrt(t))
            gamma = - (np.exp(-self.r * t) * d1 * norm.pdf(d2)) / ((self.sigma ** 2) * (self.spot ** 2) * t)
            theta = self.r * np.exp(-self.r * t) * norm.cdf(d2) + np.exp(-self.r * t) * norm.pdf(d2)
            vega = -np.exp(-self.r * t) * norm.pdf(d2) * (d1 / self.sigma)
            rho = - t * np.exp(-self.r * (t)) * norm.cdf(d2) + (np.sqrt(t)/self.sigma) * np.exp(-self.r * t) * norm.pdf(d2)

        if way == "put":
            value = np.exp(-self.r * t) * (1 - norm.cdf(d2))
            delta = - (np.exp(-self.r * t) * norm.pdf(d2)) / (self.sigma * self.spot * np.sqrt(t))
            gamma = (np.exp(-self.r * t) * d1 * norm.pdf(d2)) / (self.sigma ** 2 * self.spot * t)
            theta = self.r * np.exp(-self.r * t) * (1 - norm.cdf(d2)) - np.exp(-self.r * t) * norm.pdf(d2)
            vega = np.exp(-self.r * t) * norm.pdf(d2) * (d1 / self.sigma)
            rho = - t * np.exp(-self.r * (t)) * (1 - norm.cdf(d2)) - (np.sqrt(t)/self.sigma) * np.exp(-self.r * t) * norm.pdf(d2)

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def pricer_straddle(self, t, way, k, qty):
        # if way == "long":
        if qty >= 0:
            call = VanillaOption(k=k, t=t, style="euro", way="call")
            put = VanillaOption(k=k, t=t, style="euro", way="put")
            
        # if way =="short":
        if qty <= 0:
            call = VanillaOption(k=k, t=t, style="euro", way="call", qty=-1)
            put = VanillaOption(k=k, t=t, style="euro", way="put", qty=-1)

        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        call.pricer(model=bsm)
        put.pricer(model=bsm)


        value = call.pricing_data["value"] + put.pricing_data["value"]
        delta = call.pricing_data["delta"] + put.pricing_data["delta"]
        gamma = call.pricing_data["gamma"] + put.pricing_data["gamma"]
        vega = call.pricing_data["vega"] + put.pricing_data["vega"]
        theta = call.pricing_data["theta"] + put.pricing_data["theta"]
        rho = call.pricing_data["rho"] + put.pricing_data["rho"]


        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    
    def pricer_strangle(self, t, way, k, k2, qty):
        if qty >= 0:
            put = VanillaOption(k=k, t=t, style="euro", way="put")
            call = VanillaOption(k=k2, t=t, style="euro", way="call")
        if qty <= 0:
            call = VanillaOption(k=k, t=t, style="euro", way="call", qty=-1)
            put = VanillaOption(k=k, t=t, style="euro", way="put", qty=-1)            
        
        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        put.pricer(model=bsm)  
        call.pricer(model=bsm)

        value = call.pricing_data["value"] + put.pricing_data["value"]
        delta = call.pricing_data["delta"] + put.pricing_data["delta"]
        gamma = call.pricing_data["gamma"] + put.pricing_data["gamma"]
        vega = call.pricing_data["vega"] + put.pricing_data["vega"]
        theta = call.pricing_data["theta"] + put.pricing_data["theta"]
        rho = call.pricing_data["rho"] + put.pricing_data["rho"]

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def pricer_bull_spread(self, t, way, k, k2, qty):
        if way == "call":
            option1 = VanillaOption(k=k, t=t, style="euro", way="call")
            option2 = VanillaOption(k=k2, t=t, style="euro", way="call", qty=-1)
        if way == "put":
            option1 = VanillaOption(k=k, t=t, style="euro", way="put")
            option2 = VanillaOption(k=k2, t=t, style="euro", way="put", qty=-1)
           
        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        option1.pricer(model=bsm)  
        option2.pricer(model=bsm)

        value = option1.pricing_data["value"] + option2.pricing_data["value"]
        delta = option1.pricing_data["delta"] + option2.pricing_data["delta"]
        gamma = option1.pricing_data["gamma"] + option2.pricing_data["gamma"]
        vega = option1.pricing_data["vega"] + option2.pricing_data["vega"]
        theta = option1.pricing_data["theta"] + option2.pricing_data["theta"]
        rho = option1.pricing_data["rho"] + option2.pricing_data["rho"]       

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def pricer_bear_spread(self, t, way, k, k2, qty):
        if way == "call":
            option1 = VanillaOption(k=k, t=t, style="euro", way="call", qty=-1)
            option2 = VanillaOption(k=k2, t=t, style="euro", way="call")
        if way == "put":
            option1 = VanillaOption(k=k, t=t, style="euro", way="put", qty=-1)
            option2 = VanillaOption(k=k2, t=t, style="euro", way="put")
           
        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        option1.pricer(model=bsm)  
        option2.pricer(model=bsm)

        value = option1.pricing_data["value"] + option2.pricing_data["value"]
        delta = option1.pricing_data["delta"] + option2.pricing_data["delta"]
        gamma = option1.pricing_data["gamma"] + option2.pricing_data["gamma"]
        vega = option1.pricing_data["vega"] + option2.pricing_data["vega"]
        theta = option1.pricing_data["theta"] + option2.pricing_data["theta"]
        rho = option1.pricing_data["rho"] + option2.pricing_data["rho"]       

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def pricer_butterfly_spread(self, t, way, k, k2, k3, qty):
        if way == "long":
            option1 = VanillaOption(k=k, t=t, style="euro", way="call")
            option2 = VanillaOption(k=k2, t=t, style="euro", way="call", qty=-1)
            option3 = VanillaOption(k=k3, t=t, style="euro", way="call")
        if qty < 0:
            option1 = VanillaOption(k=k, t=t, style="euro", way="call", qty=-1)
            option2 = VanillaOption(k=k2, t=t, style="euro", way="call")
            option3 = VanillaOption(k=k3, t=t, style="euro", way="call", qty=-1)



        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        option1.pricer(model=bsm)  
        option2.pricer(model=bsm)
        option3.pricer(model=bsm)

        value = option1.pricing_data["value"] + 2 * option2.pricing_data["value"] + option3.pricing_data["value"]
        delta = option1.pricing_data["delta"] + 2 * option2.pricing_data["delta"] + option3.pricing_data["delta"]
        gamma = option1.pricing_data["gamma"] + 2 * option2.pricing_data["gamma"] + option3.pricing_data["gamma"]
        vega = option1.pricing_data["vega"] + 2 * option2.pricing_data["vega"] + option3.pricing_data["vega"]
        theta = option1.pricing_data["theta"] + 2 * option2.pricing_data["theta"] + option3.pricing_data["theta"]
        rho = option1.pricing_data["rho"] + 2 * option2.pricing_data["rho"] + option3.pricing_data["rho"]

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def pricer_strip(self, t, way, k, qty):
        
        option1 = VanillaOption(k=k, t=t, style="euro", way="call")
        option2 = VanillaOption(k=k, t=t, style="euro", way="put")

        if qty < 0:
            option1.qty = -1
            option2.qty = -1



        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        option1.pricer(model=bsm)  
        option2.pricer(model=bsm)


        value = option1.pricing_data["value"] + 2 * option2.pricing_data["value"] 
        delta = option1.pricing_data["delta"] + 2 * option2.pricing_data["delta"] 
        gamma = option1.pricing_data["gamma"] + 2 * option2.pricing_data["gamma"] 
        vega = option1.pricing_data["vega"] + 2 * option2.pricing_data["vega"] 
        theta = option1.pricing_data["theta"] + 2 * option2.pricing_data["theta"] 
        rho = option1.pricing_data["rho"] + 2 * option2.pricing_data["rho"] 

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def pricer_strap(self, t, way, k, qty):
        option1 = VanillaOption(k=k, t=t, style="euro", way="call")
        option2 = VanillaOption(k=k, t=t, style="euro", way="put")

        if qty < 0:
            option1.qty = -1
            option2.qty = -1

        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        option1.pricer(model=bsm)  
        option2.pricer(model=bsm)


        value = 2 * option1.pricing_data["value"] + option2.pricing_data["value"] 
        delta = 2 * option1.pricing_data["delta"] + option2.pricing_data["delta"] 
        gamma = 2 * option1.pricing_data["gamma"] + option2.pricing_data["gamma"] 
        vega = 2 * option1.pricing_data["vega"] + option2.pricing_data["vega"] 
        theta = 2 * option1.pricing_data["theta"] + option2.pricing_data["theta"] 
        rho = 2 * option1.pricing_data["rho"] + option2.pricing_data["rho"] 

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def pricer_calendar_spread(self, t, t2, way, k, qty):

        option1 = VanillaOption(k=k, t=t, style="euro", way="call", qty=-1)
        option2 = VanillaOption(k=k, t=t2, style="euro", way="call")

        if qty < 0:
            option1.qty = -1
            option2.qty = -1

        bsm = BlackScholesModel(spot=self.spot, r=self.r, sigma=self.sigma)
        option1.pricer(model=bsm)  
        option2.pricer(model=bsm)

        value = option1.pricing_data["value"] + option2.pricing_data["value"] 
        delta = option1.pricing_data["delta"] + option2.pricing_data["delta"] 
        gamma = option1.pricing_data["gamma"] + option2.pricing_data["gamma"] 
        vega = option1.pricing_data["vega"] + option2.pricing_data["vega"] 
        theta = option1.pricing_data["theta"] + option2.pricing_data["theta"] 
        rho = option1.pricing_data["rho"] + option2.pricing_data["rho"] 

        return {
            "spot": self.spot,
            "strike": k,
            "maturity": t,
            "value": value,           
            "sigma": self.sigma,
            "r": self.r,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "way": way,
            "model": "BlackScholes",
            "pricing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }





class BinomialModel(BaseModel):
    spot: float
    r: float
    sigma: float
    id_: UUID = Field(default_factory=uuid4)

    def pricer_vanilla(self, way, k, t, n, b):
        dt = t / n
        u = np.exp(self.sigma * np.sqrt(dt))
        d = 1 / u
        a = np.exp(b * dt)
        p = (a - d) / (u - d)
        df = np.exp(-self.r * dt)

        for i in range(0, n):
            option_value = np.max()

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