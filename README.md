# Hiram Pricing

## Overview

Hiram Pricing provides a comprehensive framework for pricing various types of options using multiple pricing models. The library features:

- Modular architecture separating market data, payoff structures, and pricing engines
- Complete Greeks calculation (Delta, Gamma, Vega, Theta, Rho)
- Extensible design for custom option types and pricing models
- Clear, intuitive API for financial professionals and quants

## Installation

```shell
pip install git+https://github.com/paulbqnt/hiram-pricing.git
```
**Requirements:** Python 3.10 or later 


## Key Features

- Vanilla Options: European and American calls and puts
- Black-Scholes Model: Industry standard closed-form solutions
- Comprehensive Greeks: First and second-order sensitivities
- Expandable Framework: Design your own option types and models




## How to price an Option:

### 1. Add your Market Data

```python
from market_data import MarketData

market = MarketData(
    spot=100.0,      # Current price of the underlying asset
    rate=0.05,       # Risk-free interest rate (5%)
    volatility=0.2,  # Volatility (20%)
    dividend=0.01    # Dividend yield (1%)
)
```

### 2. Create a payoff object

```python
from payoff import VanillaPayoff, call_payoff

option = VanillaPayoff(
    expiry=1.0,        # 1 year to expiration
    strike=105.0,      # Strike price
    payoff=call_payoff # Use the predefined call_payoff function
)
```

### 3. Choose a pricing engine

```python
from engine import BlackScholesPricingEngine, BlackScholesPricer

pricing_engine = BlackScholesPricingEngine(
    payoff_type="call",         # Type of option
    pricer=BlackScholesPricer   # Pricer
)
```

### 4. Create the option facade and price it

```python
from facade import OptionFacade

option_facade = OptionFacade(option, pricing_engine, market)
result = option_facade.price()
```

### Access the pricing results (includes greeks)


```python
print(f"Option value: {result['value']}")
print(f"Delta: {result['delta']}")
print(f"Gamma: {result['gamma']}")
print(f"Vega: {result['vega']}")
print(f"Theta: {result['theta']}")
print(f"Rho: {result['rho']}")

Option value: 7.491693155007894
Delta: 0.49687343930234723
Gamma: 0.019915806580763955
Vega: 0.3983161316152791
Theta: -0.004854766654037351
Rho: 0.44223429748583165
```

## Roadmap
- [ ] Exotic Options: Asian, barrier, lookback, and digital options
- [ ] Additional Models: Monte Carlo simulation, binomial trees, and finite difference methods
- [ ] Multi-Asset Options: Basket options, spread options, and rainbow options
- [ ] Volatility Models: Support for stochastic and local volatility models
- [ ] Performance Optimization: GPU acceleration for Monte Carlo simulations
- [ ] Interactive Visualization: Tools for visualizing pricing surfaces and sensitivities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.




