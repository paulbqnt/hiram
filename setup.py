from setuptools import setup
setup(
   name='hiram',
   version='0.0.1',
   description='An Option Pricing Library',
   author='Paul Boquant',
   author_email='paul@boquant.net',
   packages=['pandas', 'numpy', 'pydantic', 'scipy', 'yahooquery', 'streamlit', 'streamlit_extras', 'plotly', 'matplotlib', 'yfinance'],  #same as name
   install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)