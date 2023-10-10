import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Hiram Dashboard - Equity",
    page_icon="chart_with_upwards_trend",
)


@st.cache_data
def df_to_cumulative_returns(input_df):
    df_temp = input_df.copy()
    df_temp_returns = df_temp.pct_change()
    output_df = (1 + df_temp_returns).cumprod() - 1
    return output_df


class MyStreamlitEquityDashboard:
    def __init__(self):
        self.title = "Hiram Equity Dashboard"
        self.start_date = pd.to_datetime('2023-01-01')
        self.today_date = pd.to_datetime('today')
        self.ticker_list = list(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]["Symbol"])
        self.selected_stocks = []

    def run(self):
        st.title(self.title)
        self.main_content()

    def sidebar(self):
        st.sidebar.header("Sidebar")

    def main_content(self):
        st.markdown("<h6 align='left'>Made by Paul Boquant</h6>", unsafe_allow_html=True)

        cols = st.columns([2, 1, 2])
        start = cols[0].date_input('Start', value=pd.to_datetime('2023-01-01'))
        end = cols[2].date_input('End', value=pd.to_datetime('today'))

        dropdown = st.multiselect('Pick your stock', self.ticker_list, key="dropdown_stock_selector")

        # As long as no stock has been selected
        if not dropdown:
            if len(st.session_state['dropdown_stock_selector']) < 1:
                st.info(" Select one or several stocks")
                st.stop()

        trading_days = st.number_input("Select the number of days for volatility calculation", min_value=30)
        nice_dropdown = " ".join(dropdown)
        self.selected_stocks = dropdown
        print(f"self.selected_stocks:  {self.selected_stocks}")
        df_raw = yf.download(dropdown, start, end)

        df_returns = df_to_cumulative_returns(df_raw['Adj Close'])

        fig = px.line(
            df_raw['Adj Close'],
            title=f"<b>Stock price of {nice_dropdown}</b>"
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.line(
            df_returns,
            title=f"<b>Cumulative Returns of {nice_dropdown}</b>"
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Volume of {}'.format(nice_dropdown))
        df_volume = df_raw['Volume']
        st.line_chart(df_volume)

        st.subheader('Volatility of {}'.format(str(nice_dropdown)))
        df_volatility = df_raw['Close'].rolling(window=trading_days).std() * np.sqrt(trading_days)
        st.line_chart(df_volatility[trading_days:])


my_app = MyStreamlitEquityDashboard()
my_app.run()
