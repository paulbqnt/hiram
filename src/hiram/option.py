from src.hiram.pricers import OptionPricer


class Option:
    """Base class for all option types."""
    def __init__(self, payoff, expiry):
        """
        Initialize an option.

        Args:
            payoff: The payoff object defining the option's payout structure
            expiry: Time to expiration in years
        """
        self._payoff = payoff
        self._expiry = expiry


    @property
    def payoff(self): return self._payoff

    @property
    def expiry(self): return self._expiry

    @property
    def strike(self):
        if hasattr(self.payoff, 'strike'):
            return self.payoff.strike
        return None

class VanillaOption(Option):
    def __init__(self, payoff, expiry):
        super().__init__(payoff, expiry)

class EuropeanOption(VanillaOption):
    pass

class AmericanOption(VanillaOption):
    pass
