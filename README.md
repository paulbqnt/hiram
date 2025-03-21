# Hiram Pricing

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