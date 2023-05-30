import numpy as np
from typing import Optional
from pydantic import BaseModel, Field
from yahooquery import Ticker
from typing import Dict, List
from option import BlackScholes
from stock import Stock
from enum import Enum
from uuid import uuid4, UUID

class Portfolio(BaseModel):
    name: Optional[str] = None

    underlyings: Dict = {
        'stocks': {},
        'options': {},
        'bonds': {},
        'portfolios': {},
        'hedge': {}
    }

    id_: UUID = Field(default_factory=uuid4)

    def add_underlying(self, entry) -> None:
        """Add an underlying within it's correct category"""
        if isinstance(entry, BlackScholes):
            self.underlyings["options"][entry.id_] = entry

        elif isinstance(entry, Stock):
            self.underlyings["stocks"][entry.id_] = entry
        
        elif isinstance(entry, Portfolio):
            self.underlyings["portfolios"][entry.id_] = entry

    def add_hedge(self, entry) -> None:
        self.underlyings["hedge"][entry.id_] = entry
    
    def get_delta(self) -> float:
        temp_dict_delta = {}
        for option in self.underlyings["options"].values():
            if option.stock == None:
                pass
            else:
                for option in self.underlyings["options"].values():
                    # temp_dict_delta[option.stock.ticker] = {"delta": 0}
                    temp_dict_delta[option.stock.ticker] = 0
                                # populate ticker and delta in the temp dictionary
                for key, value in temp_dict_delta.items():
                    for option in self.underlyings["options"].values():
                        if key == option.stock.ticker:
                            temp_dict_delta[key] += (option.quantity * option.price) * option.delta()
                
                if len(self.underlyings["hedge"]) != 0:
                    for key, value in temp_dict_delta.items():
                        for stock in self.underlyings["hedge"].values():
                            if key == stock.ticker:
                                temp_dict_delta[key] += (stock.price * stock.quantity)

        return temp_dict_delta

    
    def get_gamma(self) -> float:
        """Return the gamma of the Portfolio"""
        delta_port = 0
        for value in self.underlyings['options'].values():
            delta_port += value.gamma() * (value.quantity * value.price)
        
        return delta_port

    def get_vega(self) -> float:
        """Return the vega of the Portfolio"""
        delta_port = 0
        for value in self.underlyings['options'].values():
            delta_port += value.vega() * (value.quantity * value.price)
        
        return delta_port

    def get_rho(self) -> float:
        """Return the rho of the Portfolio"""
        delta_port = 0
        for value in self.underlyings['options'].values():
            delta_port += value.rho() * (value.quantity * value.price)
        
        return delta_port
    
    def get_theta(self) -> float:
        """Return the theta of the Portfolio"""
        delta_port = 0
        for value in self.underlyings['options'].values():
            delta_port += value.theta() * (value.quantity * value.price)
        
        return delta_port
    
    def get_option_book_value(self) -> float:
        """Return the option book position in USD"""
        book_value = 0
        for value in self.underlyings['options'].values():
            book_value += (value.quantity * value.price)
        
        return book_value
    
    
    def get_info(self) -> str:
        """Return generic information about the portfolio"""
        
        print(f"The book value: {self.get_option_book_value()}")

        if len(self.underlyings['stocks']) > 0:
            print(f"Number of stocks in the portfolio: {len(self.underlyings['stocks'])}")

        if len(self.underlyings['options']) > 0:
            print(f"Number of options in the portfolio: {len(self.underlyings['options'])}")
            print(f"Δ:\t {round(self.get_delta(),4)}")
            print(f"Γ:\t {round(self.get_gamma(),4)}")
            print(f"θ:\t {round(self.get_theta(),4)}")
            print(f"ρ:\t {round(self.get_rho(),4)}")
            print(f"Vega:\t {round(self.get_vega(),4)}")

        if len(self.underlyings['bonds']) > 0:
            print(f"Number of bonds in the portfolio: {len(self.underlyings['bonds'])}")

        if len(self.underlyings['portfolios']) > 0:
            print(f"Number of portfolios in the portfolio: {len(self.underlyings['portfolios'])}")


    def delta_hedge(self) -> None:
        if self.get_delta == 0:
            pass
        else:   
            temp_dict = {}

            for option in self.underlyings["options"].values():
                temp_dict[option.stock.ticker] = {"price": option.stock.price, "quantity": None, "delta": 0}

            # populate ticker and delta in the temp dictionary
            for key, value in temp_dict.items():
                for option in self.underlyings["options"].values():
                    if key == option.stock.ticker:
                        value["delta"] += option.delta() * option.quantity * option.price

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
