class Portfolio:
    def __init__(self):
        self.positions = []

    def add_position(self, option, quantity, facade):
        self.positions.append((option, quantity, facade))

    def value(self):
        return sum(quantity * facade.price()["value"] for option, quantity, facade in self.positions)

    def risk_metrics(self):
        # Calculate aggregate delta, gamma, vega, etc.
        pass