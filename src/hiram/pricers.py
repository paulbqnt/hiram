from typing import Optional, ForwardRef
from src.hiram.market_data import MarketData


class OptionPricer:
    """Pure builder-pattern implementation"""

    def __init__(self,
                 option: Optional['Option'] = None,
                 engine: Optional['PricingEngine'] = None,
                 market_data: Optional[MarketData] = None):
        self._option = option
        self._engine = engine
        self._market_data = market_data

    # Builder methods
    def with_option(self, option: 'Option') -> 'OptionPricer':
        return OptionPricer(option, self._engine, self._market_data)

    def with_engine(self, engine: 'PricingEngine') -> 'OptionPricer':
        return OptionPricer(self._option, engine, self._market_data)

    def with_market_data(self, market_data: MarketData) -> 'OptionPricer':
        return OptionPricer(self._option, self._engine, market_data)

    def price(self):
        """Calculate price with basic validation"""
        if None in (self._option, self._engine, self._market_data):
            missing = []
            if self._option is None: missing.append("option")
            if self._engine is None: missing.append("engine")
            if self._market_data is None: missing.append("market_data")
            raise ValueError(f"Missing: {', '.join(missing)}")

        return self._engine.calculate(self._option, self._market_data)