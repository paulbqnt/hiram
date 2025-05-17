import numpy as np

class MarketData:
    """Simple market data container"""
    def __init__(self, spot: float, volatility: float, rate: float = 0.05, dividend: float = 0.0):
        self.spot = spot
        self.volatility = volatility
        self.rate = rate
        self.dividend = dividend


    def get_data(self) -> tuple[np.float64, np.float64, np.float64, np.float64]:
        """Returns tuple of (spot, rate, volatility, dividend) as numpy.float64"""
        return (
            np.float64(self.spot),
            np.float64(self.rate),
            np.float64(self.volatility),
            np.float64(self.dividend)
        )