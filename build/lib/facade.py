from abc import ABCMeta


class OptionFacade(object, metaclass=ABCMeta):
    """An option. -- Using Facade design pattern.  This instantiates the price method for the price engine.
    Also requires a payoff method to be used.  Requires an option, a pricing engine, and the data.
    """
    def __init__(self, option, engine, data):
        self.option = option
        self.engine = engine
        self.data = data

    def price(self):
        return self.engine.calculate(self.option, self.data)
