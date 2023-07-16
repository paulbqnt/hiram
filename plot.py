import matplotlib.pyplot as plt
import numpy as np
from option import VanillaOption
from model import BlackScholesModel


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

      print(st.shape)
      print(payoff_option.shape)
      return plt.show()

      


def plot_payoff_straddle(Straddle):
      st = np.arange(0.5*Straddle.pricing_data['spot'], 1.5 * Straddle.pricing_data['spot'])

      call = VanillaOption(k=Straddle.k, t=Straddle.t, style="euro", way="call")
      put = VanillaOption(k=Straddle.k, t=Straddle.t, style="euro", way="put")

      if Straddle.qty < 0:
            call.qty = -1
            put.qty = -1

      bsm = BlackScholesModel(spot=100, r=.05, sigma=0.3)
      call.pricer(model=bsm)
      put.pricer(model=bsm)

      name = f"{Straddle.pricing_data['way']} {Straddle.style}"

      payoff_call = vanilla_payoff(call)
      payoff_put = vanilla_payoff(put)

      fig, ax = plt.subplots()
      ax.plot(st, (payoff_put + payoff_call), label=name, color='blue')
      # plt.axvline(x=100 ,ymin=0, color = 'black', linestyle="--")
      ax.fill_between(st, (payoff_put+payoff_call), 0, where=((payoff_put+payoff_call) > 0), color='green', alpha=0.25)
      ax.fill_between(st, (payoff_put+payoff_call), 0, where=((payoff_put+payoff_call) < 0), color='red', alpha=0.25)
      
      plt.axhline(0, color = 'black', linewidth=1)
      plt.ylabel('Profit and Loss')
      plt.xlabel('spot', loc='center')
      plt.title(f"Straddle")
      plt.legend()



def plot_payoff_strangle(Strangle):
      st = np.arange(0.5*Strangle.pricing_data['spot'], 1.5 * Strangle.pricing_data['spot'])


      put = VanillaOption(k=Strangle.k, t=Strangle.t, style="euro", way="put")
      call = VanillaOption(k=Strangle.k2, t=Strangle.t, style="euro", way="call")

      if Strangle.qty < 0:
            call.qty = -1
            put.qty = -1

      bsm = BlackScholesModel(spot=100, r=.05, sigma=0.3)
      call.pricer(model=bsm)
      put.pricer(model=bsm)

      name = f"{Strangle.pricing_data['way']} {Strangle.style}"



      payoff_call = vanilla_payoff(call)
      payoff_put = vanilla_payoff(put)

      fig, ax = plt.subplots()
      ax.plot(st, (payoff_put + payoff_call), label=name, color='blue')
      # plt.axvline(x=100 ,ymin=0, color = 'black', linestyle="--")
      ax.fill_between(st, (payoff_put+payoff_call), 0, where=((payoff_put+payoff_call) > 0), color='green', alpha=0.25)
      ax.fill_between(st, (payoff_put+payoff_call), 0, where=((payoff_put+payoff_call) < 0), color='red', alpha=0.25)
      
      plt.axhline(0, color = 'black', linewidth=1)
      plt.ylabel('Profit and Loss')
      plt.xlabel('spot', loc='center')
      plt.title(f"Strangle")
      plt.legend()


def plot_payoff_bull_spread(BullSpread):
      st = np.arange(0.5*BullSpread.pricing_data['spot'], 1.5 * BullSpread.pricing_data['spot'])
      option = VanillaOption(k=BullSpread.k, t=BullSpread.t, style="euro", way="call")
      option2 = VanillaOption(k=BullSpread.k2, t=BullSpread.t, style="euro", way="call", qty=-1)      


      bsm = BlackScholesModel(spot=100, r=.05, sigma=0.3)
      option.pricer(model=bsm)
      option2.pricer(model=bsm)

      name_option = f"Long Call {round(option.k)}"
      name_option2 = f"Short Call {round(option2.k)}"
      name_srategy = f"Bull Call Spread {round(option.k)}/{round(option2.k)}"



      payoff_option = vanilla_payoff(option)
      payoff_option2 = vanilla_payoff(option2)


      fig, ax = plt.subplots()
      ax.plot(st, payoff_option, label=name_option, color='green')
      ax.plot(st, payoff_option2, label=name_option2, color='red')
      ax.plot(st, (payoff_option+payoff_option2), label=name_srategy, color='blue')
      plt.axhline(0, color = 'black', linewidth=1)
      plt.axvline(x=100 ,ymin=0, color = 'black', linestyle="--", label="spot")     

      ax.fill_between(st, (payoff_option+payoff_option2), 0, where=((payoff_option+payoff_option2) > 0), color='green', alpha=0.25)
      ax.fill_between(st, (payoff_option+payoff_option2), 0, where=((payoff_option+payoff_option2) < 0), color='red', alpha=0.25)
      plt.ylabel('Profit and Loss')
      plt.xlabel('spot', loc='center')
      plt.title(f"Bull Call Spread")
      plt.legend()



def plot_payoff_bear_spread(BearSpread):
      st = np.arange(0.5*BearSpread.pricing_data['spot'], 1.5 * BearSpread.pricing_data['spot'])
      option = VanillaOption(k=BearSpread.k, t=BearSpread.t, style="euro", way="put",qty=-1)
      option2 = VanillaOption(k=BearSpread.k2, t=BearSpread.t, style="euro", way="put")      


      bsm = BlackScholesModel(spot=100, r=.05, sigma=0.3)
      option.pricer(model=bsm)
      option2.pricer(model=bsm)

      name_option = f"Short Put {round(option.k)}"
      name_option2 = f"Long Put {round(option2.k)}"
      name_srategy = f"Bear Put Spread {round(option.k)}/{round(option2.k)}"



      payoff_option = vanilla_payoff(option)
      payoff_option2 = vanilla_payoff(option2)


      fig, ax = plt.subplots()
      ax.plot(st, payoff_option, label=name_option, color='green')
      ax.plot(st, payoff_option2, label=name_option2, color='red')
      ax.plot(st, (payoff_option+payoff_option2), label=name_srategy, color='blue')
      plt.axhline(0, color = 'black', linewidth=1)
      plt.axvline(x=100 ,ymin=0, color = 'black', linestyle="--", label="spot")     

      ax.fill_between(st, (payoff_option+payoff_option2), 0, where=((payoff_option+payoff_option2) > 0), color='green', alpha=0.25)
      ax.fill_between(st, (payoff_option+payoff_option2), 0, where=((payoff_option+payoff_option2) < 0), color='red', alpha=0.25)
      plt.ylabel('Profit and Loss')
      plt.xlabel('spot', loc='center')
      plt.title(f"Bear Put Spread")
      plt.legend()


def plot_payoff_butterfly_spread(ButterflySpread):
      st = np.arange(0.5*ButterflySpread.pricing_data['spot'], 1.5 * ButterflySpread.pricing_data['spot'])
      option = VanillaOption(k=ButterflySpread.k, t=ButterflySpread.t, style="euro", way="call")
      option2 = VanillaOption(k=ButterflySpread.k2, t=ButterflySpread.t, style="euro", way="call", qty=-1)
      option3 = VanillaOption(k=ButterflySpread.k3, t=ButterflySpread.t, style="euro", way="call")       


      bsm = BlackScholesModel(spot=100, r=.05, sigma=0.3)
      option.pricer(model=bsm)
      option2.pricer(model=bsm)
      option3.pricer(model=bsm)

      name_option = f"Long Call {round(option.k)}"
      name_option2 = f"Short 2 Call {round(option2.k)}"
      name_option3 = f"Long Call {round(option3.k)}"
      name_strategy = f"Butterfly Spread {round(option.k)}|{round(option2.k)}|{round(option3.k)}"



      payoff_option = vanilla_payoff(option)
      payoff_option2 = 2 * vanilla_payoff(option2)
      payoff_option3 = vanilla_payoff(option3)


      fig, ax = plt.subplots()
      ax.plot(st, payoff_option, label=name_option, color='green', linestyle="--", alpha=0.5)
      ax.plot(st, payoff_option2, label=name_option2, color='red', linestyle="--", alpha=0.5)
      ax.plot(st, payoff_option3, label=name_option3, color='orange', linestyle="--", alpha=0.5)      
      ax.plot(st, (payoff_option + payoff_option2 + payoff_option3), label="Butterfly Spread", color='blue')
      plt.axhline(0, color = 'black', linewidth=1)
      plt.axvline(x=100 ,ymin=0, color = 'black', linestyle="--", label="spot")     

      ax.fill_between(st, (payoff_option + payoff_option2 + payoff_option3), 0, where=((payoff_option + payoff_option2 + payoff_option3) > 0), color='green', alpha=0.25)
      ax.fill_between(st, (payoff_option + payoff_option2 + payoff_option3), 0, where=((payoff_option + payoff_option2 + payoff_option3) < 0), color='red', alpha=0.25)
      plt.ylabel('Profit and Loss')
      plt.xlabel('spot', loc='center')
      plt.title(name_strategy)

      plt.legend()