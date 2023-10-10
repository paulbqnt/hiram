import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
import yfinance as yf
import numpy as np
from facade import OptionFacade
from market_data import MarketData
from payoff import VanillaPayoff, call_payoff, put_payoff
from engine import BlackScholesPricingEngine, BlackScholesPricer, MonteCarloPricingEngine, MonteCarloPricerVanilla
import plot as hiram_plot
import plotly.express as px
st.set_page_config(page_title="Hiram Dashboard - Pricer", page_icon="chart_with_upwards_trend")
px.defaults.width = 1000
px.defaults.height = 500


def df_to_cumulative_returns(input_df):
    df_temp = input_df.copy()
    df_temp_returns = df_temp.pct_change()
    output_df = (1 + df_temp_returns).cumprod() - 1
    return output_df


def get_last_price(ticker):
    df_temp = yf.download(ticker)
    last_price = df_temp['Adj Close'][-1]
    return last_price


def get_annual_volatility(ticker):
    df_temp = yf.Ticker(ticker).history("2y")
    df_temp = df_temp['Close']
    df_temp = df_temp.pct_change()
    df_temp = df_temp[-252:]
    volatility = df_temp.std() * np.sqrt(252)
    return volatility


class MyStreamlitOptionPricer:
    def __init__(self):
        self.title = "Hiram Option Pricer"
        self.start_date = pd.to_datetime('2023-01-01')
        self.today_date = pd.to_datetime('today')
        self.ticker_list = list(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]["Symbol"])
        self.selected_stocks = []

    def run(self):
        self.main_content()

    def sidebar(self):
        st.sidebar.header("Sidebar")

    def main_content(self):
        st.header('Hiram Option Pricing Dashboard')
        st.markdown("<h6 align='left'>Made by Paul Boquant</h6>", unsafe_allow_html=True)
        selected_model = st.radio("Select which pricing model you want to use", ["Black Scholes", "Monte Carlo"])

        cols = st.columns([2, 1, 2])

        def change_spot_strike_vol():
            current_ticker = st.session_state['ticker_box_key']
            print(current_ticker)
            st.session_state["spot_box_key"] = get_last_price(current_ticker)
            st.session_state["strike_box_key"] = get_last_price(current_ticker)
            st.session_state["volatility_box_key"] = get_annual_volatility(current_ticker)

        ticker_box = cols[0].selectbox(
            "Select the stock you want to price option:",
            options=self.ticker_list,
            help="You may leave it empty",
            key="ticker_box_key",
            on_change=change_spot_strike_vol)

        option_choice = cols[2].selectbox(
            "Select the option type",
            ("call", "put"),
            key="option_choice_key"
        )

        spot_box = st.number_input(label='Spot price', value=100.0, min_value=0.0, key="spot_box_key")
        strike_box = st.number_input(label='Strike price', value=100.0, min_value=0.0, key="strike_box_key")
        volatility_box = st.number_input(label='Volatility', value=0.3, min_value=0.0, key="volatility_box_key")
        risk_free_rate_box = st.number_input(label='Risk free rate', min_value=0.0, value=0.05, key="risk_free_rate_box_key")
        maturity_box = st.number_input(label='Maturity',  min_value=0.0, value=1.0, step=0.01, key="maturity_box_key", help="in years")

        if selected_model == "Monte Carlo":
            nb_simulations = st.number_input('Number of simulations', 1000000)

        pricer_button = st.button("Price", key="pricer_button_key")

        def output_facade():
            spot = spot_box
            strike = strike_box
            risk_free_rate = risk_free_rate_box
            volatility = volatility_box
            maturity = maturity_box

            data = MarketData(spot=spot, rate=risk_free_rate, volatility=volatility, dividend=0)

            if selected_model == "Black Scholes":
                if option_choice == "call":
                    option = VanillaPayoff(expiry=maturity, strike=strike, payoff=call_payoff)
                    engine_option = BlackScholesPricingEngine("call", BlackScholesPricer)
                if option_choice == "put":
                    option = VanillaPayoff(expiry=maturity, strike=strike, payoff=put_payoff)
                    engine_option = BlackScholesPricingEngine("put", BlackScholesPricer)
            if selected_model == "Monte Carlo":
                if option_choice == "call":
                    option = VanillaPayoff(expiry=maturity, strike=strike, payoff=call_payoff)
                    engine_option = MonteCarloPricingEngine(nb_simulations, MonteCarloPricerVanilla, payoff_type="call")
                if option_choice == "put":
                    option = VanillaPayoff(expiry=maturity, strike=strike, payoff=put_payoff)
                    engine_option = MonteCarloPricingEngine(nb_simulations, MonteCarloPricerVanilla, payoff_type="put")

            BS_option = OptionFacade(option, engine_option, data)
            output = BS_option

            return output

        if not pricer_button:

            col1, col2, col3 = st.columns(3)
            col1.metric(f"{option_choice.capitalize()} Price", value=None)
            bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
            bcol1.metric("Delta", value=None)
            bcol2.metric("Gamma", value=None)
            bcol3.metric("Vega", value=None)
            bcol4.metric("Theta", value=None)
            bcol5.metric("Rho", value=None)
            add_vertical_space(2)

        else:
            facade_temp = output_facade()
            output_dict = facade_temp.price()

            col1, col2, col3 = st.columns(3)
            col1.metric(f"{option_choice.capitalize()} Price", value=round(output_dict["value"], 4))
            bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
            bcol1.metric("Delta", value=round(output_dict['delta'], 4))
            bcol2.metric("Gamma", value=round(output_dict["gamma"], 4))

            if selected_model == "Monte Carlo":
                bcol3.metric("Vega", value=round(output_dict["vega"]/100, 4))
            else:
                bcol3.metric("Vega", value=round(output_dict["vega"], 4))

            bcol4.metric("Theta", value=round(output_dict["theta"], 4))
            bcol5.metric("Rho", value=round(output_dict["rho"], 4))
            add_vertical_space(2)

            st.markdown("<h3 align='center'>Payoff Plot</h3>", unsafe_allow_html=True)
            if option_choice == "call":
                option_is_call = 1
            else:
                option_is_call = 0

            if selected_model == "Black Scholes":
                st.plotly_chart(hiram_plot.plot_payoff_vanilla(facade=facade_temp, type_plot="black_scholes"),
                                use_container_width=True)
            if selected_model == "Monte Carlo":
                st.plotly_chart(hiram_plot.plot_payoff_vanilla(facade=facade_temp, type_plot="black_scholes"),
                                use_container_width=True)

            add_vertical_space(2)
            st.markdown("<h3 align='center'>Visualization of the Greeks</h3>", unsafe_allow_html=True)

            st.plotly_chart(hiram_plot.plot_greeks(facade=facade_temp, is_call=option_is_call, type_plot="delta"), use_container_width=True)
            st.plotly_chart(hiram_plot.plot_greeks(facade=facade_temp, is_call=option_is_call, type_plot="gamma"), use_container_width=True)
            st.plotly_chart(hiram_plot.plot_greeks(facade=facade_temp, is_call=option_is_call, type_plot="vega"), use_container_width=True)
            st.plotly_chart(hiram_plot.plot_greeks(facade=facade_temp, is_call=option_is_call, type_plot="theta"), use_container_width=True)
            st.plotly_chart(hiram_plot.plot_greeks(facade=facade_temp, is_call=option_is_call, type_plot="rho"), use_container_width=True)


my_app = MyStreamlitOptionPricer()
my_app.run()
