import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

from src.hiram_pricing.market_data import MarketData
from payoff import CallPayoff, PutPayoff
from engine import BlackScholesPricingEngine, BlackScholesPricer
from facade import OptionFacade

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
    if type_plot == "black_scholes":
            st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
            payoff_option = vanilla_payoff(facade)
            mask = payoff_option >= 0
            payoff_above = np.where(mask, payoff_option, 0)
            payoff_below = np.where(mask, 0, payoff_option)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=st, y=payoff_above, fill='tozeroy', fillcolor="rgba(147, 250, 165, 0.5)", mode='none'))
            fig.add_trace(go.Scatter(x=st, y=payoff_below, fill='tozeroy', fillcolor="rgba(242, 38, 19, 0.5)", mode='none'))
            fig.update_traces(showlegend=False)
            return fig
    elif type_plot == "monte_carlo":
            st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
            payoff_option = vanilla_payoff(facade)
            mask = payoff_option >= 0
            payoff_above = np.where(mask, payoff_option, 0)
            payoff_below = np.where(mask, 0, payoff_option)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=st, y=payoff_above, fill='tozeroy', fillcolor="rgba(147, 250, 165, 0.5)", mode='none'))
            fig.add_trace(go.Scatter(x=st, y=payoff_below, fill='tozeroy', fillcolor="rgba(242, 38, 19, 0.5)", mode='none'))
            fig.update_traces(showlegend=False)
            return fig



        #     (fig, ax) = plt.subplots()
        #
        #     ax.plot(st, payoff_option, color='dodgerblue')
        #     ax.fill_between(st, payoff_option, 0, where=(payoff_option > 0), color='green', alpha=0.25)
        #     ax.fill_between(st, payoff_option, 0, where=(payoff_option < 0), color='red', alpha=0.25)
        #     plt.axhline(0, color='black', linewidth=1)
        #     plt.ylabel('Profit and loss')
        #     plt.xlabel('S', loc='center')
        #     plt.title(f"{facade.engine.payoff_type.capitalize()} Spot:{round(facade.data.spot, 2)} Strike:{round(facade.option.strike, 2)}")
        #     # plt.legend()
        #     print(facade.engine.payoff_type)
        #     return plt.show()
        # case _:
        #     raise ValueError(f'"{type_plot}" is not a correct payoff type, please select one of these: black_scholes/monte_carlo')




# def plot_payoff_vanilla(facade, type_plot):
#     '''Get an option facade and a type_plot as input and return a vanilla plot payoff'''
#     match type_plot:
#         case "black_scholes":
#             st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
#             payoff_option = vanilla_payoff(facade)
#             (fig
#              , ax) = plt.subplots()
#
#             ax.plot(st, payoff_option, color='dodgerblue')
#             ax.fill_between(st, payoff_option, 0, where=(payoff_option > 0), color='green', alpha=0.25)
#             ax.fill_between(st, payoff_option, 0, where=(payoff_option < 0), color='red', alpha=0.25)
#             plt.axhline(0, color='black', linewidth=1)
#             plt.ylabel('Profit and loss')
#             plt.xlabel('S', loc='center')
#             plt.title(f"{facade.engine.payoff_type.capitalize()} Spot:{round(facade.data.spot, 2)} Strike:{round(facade.option.strike, 2)}")
#             # plt.legend()
#             print(facade.engine.payoff_type)
#             return plt.show()
#         case _:
#             raise ValueError(f'"{type_plot}" is not a correct payoff type, please select one of these: black_scholes/monte_carlo')
#




def plot_greeks(facade, is_call, type_plot):
    '''Get an option facade and a greek_type as input and return a greek plot'''
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
    delta_values = []
    gamma_values = []
    theta_values = []
    vega_values = []
    rho_values = []

    if is_call == 1:
        option_output = CallPayoff(expiry=facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
        payoff_type = "call"
    elif is_call == 0:
        option_output = PutPayoff(expiry=.2, strike=100, payoff=put_payoff)
        payoff_type = "put"

    engine = BlackScholesPricingEngine(payoff_type, BlackScholesPricer)

    # if type(facade.engine) == MonteCarloPricingEngine:
    #     engine = MonteCarloPricingEngine(100000, MonteCarloPricerVanilla)
    #
    # elif type(facade.engine) == BlackScholesPricingEngine:
    #     engine = BlackScholesPricingEngine(payoff_type, BlackScholesPricer)

    for s in st:
        data = MarketData(spot=s, rate=facade.data.rate, volatility=facade.data.volatility, dividend=facade.data.dividend)
        option_facade = OptionFacade(option_output , engine, data)
        pricing_output = option_facade.price()

        delta_values.append(pricing_output["delta"])
        gamma_values.append(pricing_output["gamma"])
        theta_values.append(pricing_output["theta"])
        vega_values.append(pricing_output["vega"])
        rho_values.append(pricing_output["rho"])
    if type_plot == "delta":
        selected_greek = delta_values
    if type_plot == "gamma":
        selected_greek = gamma_values
    if type_plot == "theta":
        selected_greek = theta_values
    if type_plot == "vega":
        selected_greek = vega_values
    if type_plot == "rho":
        selected_greek = rho_values

    fig = px.line(
        x = st,
        y = selected_greek,
        labels = dict(x = "Underlying Asset Price", y = f"{type_plot.capitalize()}")

    )
    fig.update_layout(title_text=f'{type_plot.capitalize()}', title_x=0.5)
    return fig



def plot_payoff_straddle(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot) \

    call_temp = CallPayoff(expiry =facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
    put_temp = PutPayoff(expiry =facade.option.expiry, strike=facade.option.strike, payoff=put_payoff)

    BS_call_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_put_engine = BlackScholesPricingEngine("put", BlackScholesPricer)

    BS_call = OptionFacade(call_temp, BS_call_engine, facade.data)
    BS_put = OptionFacade(put_temp, BS_put_engine, facade.data)

    payoff_option_call = vanilla_payoff(BS_call)
    payoff_option_put = vanilla_payoff(BS_put)

    fig, ax = plt.subplots()
    ax.plot(st, (payoff_option_call + payoff_option_put), label='straddle payoff', color='blue')

    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) > 0), color='green', alpha=0.25)
    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) < 0), color='red', alpha=0.25)

    plt.axhline(0, color='black', linewidth=1)
    plt.ylabel('Profit and Loss')
    plt.xlabel('spot', loc='center')
    plt.title(f"Straddle")
    return plt.show()


def plot_payoff_strangle(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot) \

    put_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike, payoff=put_payoff)
    call_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike_2, payoff=call_payoff)

    BS_put_engine = BlackScholesPricingEngine("put", BlackScholesPricer)
    BS_call_engine = BlackScholesPricingEngine("call", BlackScholesPricer)

    BS_put = OptionFacade(put_temp, BS_put_engine, facade.data)
    BS_call = OptionFacade(call_temp, BS_call_engine, facade.data)

    payoff_option_put = vanilla_payoff(BS_put)
    payoff_option_call = vanilla_payoff(BS_call)

    fig, ax = plt.subplots()
    ax.plot(st, (payoff_option_call + payoff_option_put), label='straddle payoff', color='blue')

    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) > 0), color='green', alpha=0.25)
    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) < 0), color='red', alpha=0.25)

    plt.axhline(0, color='black', linewidth=1)
    plt.ylabel('Profit and Loss')
    plt.xlabel('spot', loc='center')
    plt.title(f"Strangle")
    return plt.show()


def plot_payoff_bull_spread(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)

    option1_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
    option2_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike_2, payoff=call_payoff)

    BS_option1_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_option2_engine = BlackScholesPricingEngine("call", BlackScholesPricer)

    BS_option1= OptionFacade(option1_temp, BS_option1_engine, facade.data)
    BS_option2 = OptionFacade(option2_temp, BS_option2_engine, facade.data)

    payoff_option1 = vanilla_payoff(BS_option1)
    payoff_option2 = -vanilla_payoff(BS_option2)

    fig, ax = plt.subplots()
    ax.plot(st, payoff_option1, label='long call', color='green', linestyle="--", alpha=0.5)
    ax.plot(st, payoff_option2, label='short call', color='red', linestyle="--", alpha=0.5)
    ax.plot(st, (payoff_option1 + payoff_option2), label='bull spread', color='blue')
    plt.axhline(0, color='black', linewidth=1)

    ax.fill_between(st, (payoff_option1 + payoff_option2), 0, where=((payoff_option1 + payoff_option2) > 0), color='green', alpha=0.25)
    ax.fill_between(st, (payoff_option1 + payoff_option2), 0, where=((payoff_option1 + payoff_option2) < 0), color='red', alpha=0.25)
    plt.ylabel('Profit and Loss')
    plt.xlabel('spot', loc='center')
    plt.title(f"Bull Spread")
    plt.legend()
    return plt.show()


def plot_payoff_bear_spread(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot) \

    option1_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
    option2_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike_2, payoff=call_payoff)

    BS_option1_engine = BlackScholesPricingEngine("put", BlackScholesPricer)
    BS_option2_engine = BlackScholesPricingEngine("put", BlackScholesPricer)

    BS_option1= OptionFacade(option1_temp, BS_option1_engine, facade.data)
    BS_option2 = OptionFacade(option2_temp, BS_option2_engine, facade.data)

    payoff_option1 = -vanilla_payoff(BS_option1)
    payoff_option2 = vanilla_payoff(BS_option2)

    fig, ax = plt.subplots()
    ax.plot(st, payoff_option1, label='short put', color='green', linestyle="--", alpha=0.5)
    ax.plot(st, payoff_option2, label='long put', color='red', linestyle="--", alpha=0.5)
    ax.plot(st, (payoff_option1 + payoff_option2), label='bear spread', color='blue')
    plt.axhline(0, color='black', linewidth=1)

    ax.fill_between(st, (payoff_option1 + payoff_option2), 0, where=((payoff_option1 + payoff_option2) > 0), color='green', alpha=0.25)
    ax.fill_between(st, (payoff_option1 + payoff_option2), 0, where=((payoff_option1 + payoff_option2) < 0), color='red', alpha=0.25)
    plt.ylabel('Profit and Loss')
    plt.xlabel('spot', loc='center')
    plt.title(f"Bear Spread")
    plt.legend()
    return plt.show()

def plot_payoff_butterfly_spread(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot) \

    option1_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
    option2_temp = VanillaPayoff(expiry =facade.option.expiry, strike=facade.option.strike_2, payoff=call_payoff)
    option3_temp = VanillaPayoff(expiry=facade.option.expiry, strike=facade.option.strike_3, payoff=call_payoff)

    BS_option1_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_option2_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_option3_engine = BlackScholesPricingEngine("call", BlackScholesPricer)

    BS_option1 = OptionFacade(option1_temp, BS_option1_engine, facade.data)
    BS_option2 = OptionFacade(option2_temp, BS_option2_engine, facade.data)
    BS_option3 = OptionFacade(option3_temp, BS_option3_engine, facade.data)

    payoff_option1 = vanilla_payoff(BS_option1)
    payoff_option2 = -2 * vanilla_payoff(BS_option2)
    payoff_option3 = vanilla_payoff(BS_option3)

    fig, ax = plt.subplots()
    ax.plot(st, payoff_option1, label='long call', color='green', linestyle="--", alpha=0.5)
    ax.plot(st, payoff_option2, label='short 2 calls', color='red', linestyle="--", alpha=0.5)
    ax.plot(st, payoff_option3, label='long call', color='orange', linestyle="--", alpha=0.5)
    ax.plot(st, (payoff_option1 + payoff_option2 + payoff_option3), label="Butterfly Spread", color='blue')
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(x=100, ymin=0, color='black', linestyle="--", label="spot")

    return plt.show()

def plot_payoff_strip(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
    call_temp = VanillaPayoff(expiry=facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
    put_temp = VanillaPayoff(expiry=facade.option.expiry, strike=facade.option.strike, payoff=put_payoff)

    BS_call_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_put_engine = BlackScholesPricingEngine("put", BlackScholesPricer)

    BS_call = OptionFacade(call_temp, BS_call_engine, facade.data)
    BS_put = OptionFacade(put_temp, BS_put_engine, facade.data)

    payoff_option_call = vanilla_payoff(BS_call)
    payoff_option_put = 2 * vanilla_payoff(BS_put)

    fig, ax = plt.subplots()
    ax.plot(st, (payoff_option_call + payoff_option_put), label='straddle payoff', color='blue')

    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) > 0), color='green', alpha=0.25)
    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) < 0), color='red', alpha=0.25)

    plt.axhline(0, color='black', linewidth=1)
    plt.ylabel('Profit and Loss')
    plt.xlabel('spot', loc='center')
    plt.title(f"Strip")
    return plt.show()

def plot_payoff_strap(facade):
    st = np.arange(0.5 * facade.data.spot, 1.5 * facade.data.spot)
    call_temp = VanillaPayoff(expiry=facade.option.expiry, strike=facade.option.strike, payoff=call_payoff)
    put_temp = VanillaPayoff(expiry=facade.option.expiry, strike=facade.option.strike, payoff=put_payoff)

    BS_call_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_put_engine = BlackScholesPricingEngine("put", BlackScholesPricer)

    BS_call = OptionFacade(call_temp, BS_call_engine, facade.data)
    BS_put = OptionFacade(put_temp, BS_put_engine, facade.data)

    payoff_option_call = 2 * vanilla_payoff(BS_call)
    payoff_option_put = vanilla_payoff(BS_put)

    fig, ax = plt.subplots()
    ax.plot(st, (payoff_option_call + payoff_option_put), label='straddle payoff', color='blue')

    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) > 0), color='green', alpha=0.25)
    ax.fill_between(st, (payoff_option_call + payoff_option_put), 0, where=((payoff_option_call + payoff_option_put) < 0), color='red', alpha=0.25)

    plt.axhline(0, color='black', linewidth=1)
    plt.ylabel('Profit and Loss')
    plt.xlabel('spot', loc='center')
    plt.title(f"Strap")
    return plt.show()
