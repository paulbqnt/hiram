import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Hiram! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

ticker_box = st.selectbox(
    'Select the stock on which you want to price an option: (you may leave it empty)',
    [0.4, 0.5, 0.8],
    index=None)



volatility_box_value = 0.3

if ticker_box is not None:
    volatility_box = st.number_input('Volatility', value = ticker_box)
else:
    volatility_box = st.number_input('Volatility', value=volatility_box_value)

