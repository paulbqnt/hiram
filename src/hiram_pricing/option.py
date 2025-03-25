

class Option:
    def __init__(self, payoff, expiry):
        self.payoff = payoff
        self.expiry = expiry

    @property
    def strike(self):
        # Delegate to payoff if it has a strike
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


class OptionStrategy(Option):
    def __init__(self, options_list):
        self.options = options_list

    def payoff(self, spot_price):
        return sum(option.payoff(spot_price) for option in self.options)