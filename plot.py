import matplotlib.pyplot as plt
import numpy as np
from option import VanillaOption


def vanilla_payoff(Option):
    st = np.arange(0.5*Option.pricing_data['spot'], 1.5*Option.pricing_data['spot'])
    premium = Option.pricing_data['value']
    strike = Option.pricing_data['strike']

    if Option.way == "call":
          if Option.qty > 0:
               return np.where(st > strike, st - strike, 0) - premium
          elif Option.qty < 0:
                return np.where(st > strike, strike-st, 0) + premium
          
    if Option.way == "put":
          if Option.qty > 0:
                return np.where(strike > st, strike - st, 0) - premium
          if Option.qty < 0:
                return np.where(st < strike, st - strike, 0) + premium


def plot_payoff_vanilla(Option):
        st = np.arange(0.5*Option.pricing_data['spot'], 1.5*Option.pricing_data['spot'])
        payoff_option = vanilla_payoff(Option)
        fig, ax = plt.subplots()
        ax.plot(st, payoff_option, label=Option.way, color='dodgerblue')
        ax.fill_between(st, payoff_option, 0, where=(payoff_option > 0), color='green', alpha=0.25)
        ax.fill_between(st, payoff_option, 0, where=(payoff_option < 0), color='red', alpha=0.25)
        plt.axhline(0, color = 'black', linewidth=1)
        plt.ylabel('Profit and loss')
        plt.xlabel('S', loc='center')
        plt.title(f"Spot: {round(Option.pricing_data['spot'])} Strike: {round(Option.pricing_data['strike'])}")
        plt.legend()

        return plt.show()



def digital_payoff(Option):
      pass

    
    