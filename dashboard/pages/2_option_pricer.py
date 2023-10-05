import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
import yfinance as yf
import numpy as np

st.set_page_config(
    page_title="Hiram Dashboard",
    page_icon="chart_with_upwards_trend",
)


def df_to_cumulative_returns(input_df):
    df_temp = input_df.copy()
    df_temp_returns = df_temp.pct_change()
    output_df = (1 + df_temp_returns).cumprod() - 1
    return output_df


def get_last_price(ticker):
    df_temp = yf.Ticker(ticker).history()
    last_price = df_temp['Close'].iloc[-1]
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
        # self.df_raw = yf.download(self.start_date, self.today_date)['Adj Close']
        self.selected_stocks = []

    def run(self):
        # st.title(self.title)

        # self.sidebar()
        self.main_content()

    def sidebar(self):
        st.sidebar.header("Sidebar")
        # Add widgets and controls to the sidebar here

    def main_content(self):
        st.header('Hiram Option Pricing Dashboard')
        selected_model = st.radio("Select which pricing model you want to use", ["Black Scholes", "Monte Carlo"])

        cols = st.columns([2, 1, 2])

        def change_spot_strike_vol():
            last_price = get_last_price(ticker_box)
            st.session_state["spot_box_key"] = last_price
            st.session_state["strike_box_key"] = last_price
            st.session_state["volatility_box_key"] = get_annual_volatility(ticker_box)


        ticker_box = cols[0].selectbox(
            "Select the stock you want to price option:",
            options=self.ticker_list,
            help="You may leave it empty",
            key="ticker_box_key",
            on_change=change_spot_strike_vol)

        option_choice = cols[2].selectbox(
            "select the option type",
            ("Call", "Put"),
            key="option_choice_key"
        )

        spot_box = st.number_input(label='Spot price', value=100.0, min_value=0.0, key="spot_box_key")

        strike_box = st.number_input(label='Strike price', value=100.0, min_value=0.0, key="strike_box_key")
        volatility_box = st.number_input(label='Volatility', value=0.3, min_value=0.0, key="volatility_box_key")
        risk_free_rate_box = st.number_input(label='Risk free rate', min_value=0.0, value=0.05, key="risk_free_rate_box_key")
        maturity_box = st.number_input(label='Maturity',  min_value=0.0, value=1.0, step=0.01, key="maturity_box_key", help="in years")

        if selected_model == "Monte Carlo":
            nb_simulations = st.number_input('Number of simulations', 1000000)

        pricer_button = st.button("Price")

        add_vertical_space(2)
        st.markdown("<h3 align='center'>Option Prices and Greeks</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric(f"{option_choice} Price", value=None)

        bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)

        bcol1.metric("Delta", value=None)
        bcol2.metric("Gamma", value=None)
        bcol3.metric("Vega", value=None)
        bcol4.metric("Theta", value=None)
        bcol5.metric("Rho", value=None)
        add_vertical_space(2)

        st.markdown("<h3 align='center'>Visualization of the Greeks</h3>", unsafe_allow_html=True)



        # spot_box_value = 100
        # strike_box_value = 100
        # volatility_box_value = 0.3
        # risk_free_rate_box_value = 0.05
        # maturity_box_value = 1
        #
        # if ticker_box:
        #     spot_box = st.number_input('Spot price', get_last_price(ticker_box))
        #     volatility_box = st.number_input('Volatility', get_annual_volatility(ticker_box))
        # else:
        #     spot_box = st.number_input('Spot price', value=spot_box_value)
        #     volatility_box = st.number_input('Volatility', value=0.3)
        #
        # strike_box = st.number_input('Strike price', strike_box_value)
        #
        # risk_free_rate_box = st.number_input('Risk free rate', risk_free_rate_box_value)
        # maturity_box = st.number_input('Maturity', maturity_box_value)
        #
        # if selected_model == "Monte Carlo":
        #     nb_simulations = st.number_input('Number of simulations', 1000000)
        #
        #
        # pricer_button = st.button("Price")
        #
        # add_vertical_space(2)
        # st.markdown("<h3 align='center'>Option Prices and Greeks</h3>", unsafe_allow_html=True)
        #
        # col1, col2, col3 = st.columns(3)
        # col1.metric(f"{option_choice} Price", value=None)
        #
        # bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
        #
        # bcol1.metric("Delta", value=None)
        # bcol2.metric("Gamma", value=None)
        # bcol3.metric("Vega", value=None)
        # bcol4.metric("Theta", value=None)
        # bcol5.metric("Rho", value=None)
        #
        # st.markdown("<h3 align='center'>Visualization of the Greeks</h3>", unsafe_allow_html=True)
        #



my_app = MyStreamlitOptionPricer()
my_app.run()