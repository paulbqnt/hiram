import facade
from facade import OptionFacade

class Plot:
    def __init__(self, facade : OptionFacade):
        self.__facade = facade
        self.data = self.__facade.data
        self.engine = self.__facade.engine

    def show(self, choice):
        if choice == "payoff":
            plot_payoff(self.data)
        else:
            raise ValueError("You must pass a valid choice.")

def plot_payoff(facade):
    print(facade)
