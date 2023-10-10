from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hiram",
    version="0.0.1",
    description="An Option Pricing Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="paulbqnt (Paul Boquant)",
    email="paul@boquant.net",
    license="MIT",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'yfinance', 'scipy', 'plotly', 'matplotlib', 'yahooquery']
)
