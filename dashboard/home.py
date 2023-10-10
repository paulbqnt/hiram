import streamlit as st
from utils import add_logo
import pandas as pd
st.set_page_config(
    page_title="Hiram Dashboard - Home",
    page_icon="chart_with_upwards_trend",
)



st.write("# Welcome to Hiram! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Hiram is a free financial library built in python that can be used for option pricing 
    and financial products management. Hiram is specifically useful students and junior practitioners.
    
    **👈 Select a demo from the sidebar** to see some examples
    of what Hiram Dashboard can do!
    
    ### Overview
    Let's consider you are an option market maker on the S&P 500, this dashboard will help you to:
    1. Check the recent **underlying stock behavior** (price, historical vol, volume traded)
    2. Price options with both **Black Scholes Merton** and **Monte-Carlo**
    3. Check the Greeks of the option
    4. Generate marketing documents in PDF (working on it..)
    
    
    ### Want to learn more?
    - Check out the [github repo](https://github.com/paulbqnt/hiram)
    - See all my other projects here: [github profile](https://github.com/paulbqnt/)
    - Jump into my [website](https://paulboquant.com/)
    - Ask me a question on [Linkedin](https://www.linkedin.com/in/paulboquant/)
    """
)