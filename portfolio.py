from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict 
from option impot VanillaOption
from stock import Stock
from uuid import uuid4, UUID

class Portfolio(BaseModel):
    name: Optional[str] = None
    underlyings: Dict = {
        "options": {},
        "stocks": {},
        "hedge": {}
    }
    id_: UUID = Field(default_factory=uuid4)
    

    def add_underlying(self, entry) -> None:
        if isinstance(entry, VanillaOption):
            self.underlyings["options"][entry.id_] = entry

        if isinstance(entry, Stock):
            self.underlyings["stocks"][entry.id_] = entry
    

    def add_hedge(self, entry) -> None:
        self.underlyings["hedge"][entry.id_] = entry


    def get_delta(self) -> dict:
        delta = 0
        for option in self.underlyings["options"].values():
            delta += option.pricing_data["delta"] * abs(option.price * option.qty)
        return delta
    

    def get_gamma(self) -> float:
        gamma = 0
        for option in self.underlyings["options"].values():
            gamma += option.pricing_data["gamma"] * abs(option.price * option.qty)
        return gamma


    def get_vega(self) -> float:
        vega = 0
        for option in self.underlyings['options'].values():
            vega += option.pricing_data["vega"] * abs(option.price * option.qty)
        return vega


    def get_rho(self) -> float:
        rho = 0
        for option in self.underlyings['options'].values():
            rho += option.pricing_data["rho"] * abs(option.price * option.qty)
        return rho
    

    def get_theta(self) -> float:
        """Return the theta of the Portfolio"""
        theta = 0
        for option in self.underlyings['options'].values():
            theta += option.pricing_data["theta"] * abs(option.price * option.qty)
        
        return theta
    

    def get_option_book_value(self) -> float:
        """Return the option book position"""
        option_book_value = 0
        for option in self.underlyings['options'].values():
            option_book_value += (option.price * option.qty)
        
        return option_book_value


    def delta_hedge(self):
        temp_dict = {}
        
        for option in self.underlyings["options"].values():
            temp_dict[option.stock.ticker] = {"price": option.stock.price, "quantity": None, "delta": 0}

        
        # populate ticker and delta in the temp dictionary
        for key, value in temp_dict.items():
            for option in self.underlyings["options"].values():
                if key == option.stock.ticker:
                    value["delta"] = option.pricing_data.get('delta') * abs(option.qty * option.price)
                        
        # compute the number of stocks for delta hedging
        for key, value in temp_dict.items():
            if value["delta"] < 0:
                value["quantity"] = abs(value["delta"] / value["price"])
            elif value["delta"] > 0:
                value["quantity"] = -value["delta"] / value["price"]

        # add stock into the hedging part of the portfolio for complete delta hedging
        for key, value in temp_dict.items():
            temp_stock = Stock(ticker=key, price=value["price"], quantity=value["quantity"])
            self.add_hedge(temp_stock)
            print(f"{temp_stock.quantity} {temp_stock.ticker} added into the hedging part")