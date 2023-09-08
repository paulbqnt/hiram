import facade
import old_payoff
from facade import OptionFacade
from market_data import MarketData
from old_payoff import VanillaPayoff, call_payoff, put_payoff
from engine import BlackScholesPricingEngine, BlackScholesPricer

import matplotlib.pyplot as plt
import numpy as np

class Plot:
    def __init__(self, facade : OptionFacade):
        self.__facade = facade
        self.data = self.__facade.data
        self.engine = self.__facade.engine

    def show(self, choice):
        if choice == "payoff":
            self.plot_payoff(self.data)
        else:
            raise ValueError("You must pass a valid choice.")


def vanilla_payoff(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
    premium = facade.price().get("value")
    strike = facade.option.strike
    if facade.engine.payoff_type == "call":
        return np.where(st > strike, st - strike, 0) - premium
    if facade.engine.payoff_type == "put":
        return np.where(strike > st, strike - st, 0) - premium

def plot_payoff_vanilla(facade, type_plot):
    '''Get an option facade and a type_plot as input and return a vanilla plot payoff'''
    match type_plot:
        case "black_scholes":
            st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
            payoff_option = vanilla_payoff(facade)
            fig, ax = plt.subplots()

            ax.plot(st, payoff_option, color='dodgerblue')
            ax.fill_between(st, payoff_option, 0, where=(payoff_option > 0), color='green', alpha=0.25)
            ax.fill_between(st, payoff_option, 0, where=(payoff_option < 0), color='red', alpha=0.25)
            plt.axhline(0, color='black', linewidth=1)
            plt.ylabel('Profit and loss')
            plt.xlabel('S', loc='center')
            plt.title(f"{facade.engine.payoff_type.capitalize()} Spot:{facade.data.spot} Strike:{facade.option.strike}")
            # plt.legend()
            print(facade.engine.payoff_type)
            return plt.show()
        case _:
            raise ValueError(f'"{type_plot}" is not a correct payoff type, please select one of these: black_scholes/monte_carlo')


def plot_payoff_straddle(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)

    def call_straddle():
        call_temp = VanillaPayoff(expiry=.25, strike=40.0, payoff=call_payoff)
        put_temp = VanillaPayoff(expiry=.25, strike=40.0, payoff=put_payoff)

        BS_call_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
        BS_put_engine = BlackScholesPricingEngine("put", BlackScholesPricer)

        BS_call = OptionFacade(call_temp, BS_call_engine, facade.data)
        BS_put = OptionFacade(put_temp, BS_put_engine, facade.data)





    return call_straddle()


    #     st = np.arange(0.5 * Straddle.pricing_data['spot'], 1.5 * Straddle.pricing_data['spot'])
    #
    #     call = VanillaOption(k=Straddle.k, t=Straddle.t, style="euro", way="call")
    #     put = VanillaOption(k=Straddle.k, t=Straddle.t, style="euro", way="put")
    #
    #     if Straddle.qty < 0:
    #         Straddle.way = "short"
    #         call.qty = -1
    #         put.qty = -1
    #
    #     bsm = BlackScholesModel(spot=Straddle.pricing_data['spot'], r=Straddle.pricing_data['r'],
    #                             sigma=Straddle.pricing_data['sigma'])
    #     call.pricer(model=bsm)
    #     put.pricer(model=bsm)
    #
    #     name = f"{Straddle.way} {Straddle.style}"
    #
    #     payoff_call = vanilla_payoff(call)
    #     payoff_put = vanilla_payoff(put)
    #
    #     fig, ax = plt.subplots()
    #     ax.plot(st, (payoff_put + payoff_call), label=name, color='blue')
    #     # plt.axvline(x=100 ,ymin=0, color = 'black', linestyle="--")
    #     ax.fill_between(st, (payoff_put + payoff_call), 0, where=((payoff_put + payoff_call) > 0), color='green',
    #                     alpha=0.25)
    #     ax.fill_between(st, (payoff_put + payoff_call), 0, where=((payoff_put + payoff_call) < 0), color='red',
    #                     alpha=0.25)
    #
    #     plt.axhline(0, color='black', linewidth=1)
    #     plt.ylabel('Profit and Loss')
    #     plt.xlabel('spot', loc='center')
    #     plt.title(f"Straddle")
    #     plt.legend()







    # if type_plot == "monte_carlo":
    #     st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
    #     premium = facade.price().get('value')
    #     strike = facade.option.strike
    #     return facade.option.payoff
    #

    # print(payoff.VanillaPayoff.payoff)


    #
    # if Option.way == "call":
    #     if Option.qty > 0:
    #         return np.where(st > strike, st - strike, 0) - premium
    #     elif Option.qty < 0:
    #         return np.where(st > strike, strike - st, 0) + premium
    #
    # if Option.way == "put":
    #     if Option.qty > 0:
    #         return np.where(strike > st, strike - st, 0) - premium
    #     if Option.qty < 0:
    #         return np.where(st < strike, st - strike, 0) + premium