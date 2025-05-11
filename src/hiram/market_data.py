from pydantic import BaseModel, Field
from typing import Tuple
import numpy as np


class MarketData(BaseModel):
    """
    Represents market data parameters for financial modeling.

    This class encapsulates and validates the essential market parameters
    used in financial modeling and derivatives pricing. All values are
    stored as NumPy float64.

    Attributes:
        spot: The current market price of the underlying asset
        rate: The risk-free interest rate (annualized)
        volatility: The volatility of the underlying asset (annualized)
        dividend: The dividend yield of the underlying asset (annualized)
    """
    spot: float = Field(gt=0, description="Spot price of the underlying asset")
    rate: float = Field(ge=0, description="Risk-free interest rate")
    volatility: float = Field(gt=0, description="Volatility of the underlying asset")
    dividend: float = Field(ge=0, description="Dividend yield")

    class Config:
        """Pydantic config"""
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.spot = np.float64(self.spot)
        self.rate = np.float64(self.rate)
        self.volatility = np.float64(self.volatility)
        self.dividend = np.float64(self.dividend)

    def get_data(self) -> Tuple[np.float64, np.float64, np.float64, np.float64]:
        """
        Returns a tuple containing all market data parameters as numpy.float64.

        Returns:
            Tuple[np.float64, np.float64, np.float64, np.float64]: A tuple containing
            (spot, rate, volatility, dividend) in that order.
        """
        return self.spot, self.rate, self.volatility, self.dividend