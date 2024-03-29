# HIRAM
**Hiram** is a free financial library built in  python that can be used for **Equity Option Pricing**.

---
## How to use it

### Let's price a Call option

```python 
from hiram.facade import OptionFacade
from hiram.market_data import MarketData
from hiram.payoff import VanillaPayoff, call_payoff
from hiram.engine import BlackScholesPricingEngine, BlackScholesPricer

data = MarketData(spot=100, rate=0.05, volatility=.35, dividend=0)

call = VanillaPayoff(expiry=.2, strike=100, payoff=call_payoff)

BS_engine_call = BlackScholesPricingEngine("call", BlackScholesPricer)

BS_call = OptionFacade(call, BS_engine_call, data)
print(f"call: {BS_call.price()}")
```
### Output
```python
call: {'value': 6.717176287682648, 'delta': 0.550981792606417, 'gamma': 0.025231275699541374,
       'vega': 0.17661892989678962, 'theta': -0.03563676416970135, 'rho': 0.07898638667249831}}
```


--- 

### To-Do
- **Black Scholes**: Strategies
  - IronCondor
- **Portfolio Class** (add methods)
- **Stock Class** (add methods)
- **Plot Class**
- **Bond Class** : Zero-Coupon Bond
- **Black Scholes**: Asian Vanilla Options
- **Monte Carlo**: Asian Vanilla Options
- **Black Scholes**: Digital Options
- **Monte Carlo**: Digital Options
 **Black Scholes**: Barrier Options
- **Monte Carlo**: Barrier Options
- **Binomial Model** (American/European)
- **Lookback Options**
- **Chooser Options**
- **Ratchet Options**
--- 

### Implemented

#### Engine
- [X] **Black Scholes**: Vanilla **Call** & **Put**  (plot :white_check_mark: )
- [X] **Monte-Carlo**: Vanilla Call & Put (plot :white_check_mark: )
- [X] **Black Scholes**: Strategy **Straddle** (plot :white_check_mark: )
- [X] **Black Scholes**: Strategy **Strangle** (plot :white_check_mark: )
- [X] **Black Scholes**: Strategy **Butterfly Spread** (plot :white_check_mark: )
- [X] **Black Scholes**: Strategy **Strip** & **Strap** (plot :white_check_mark: )
- [X] **Black Scholes**: Strategy **Calendar Spread**

#### Stock
##### Methods
- [X] **fetch history**
- [X] **historical volatility**
- [X] **parkinson historic volatility**
- [X] **rogers satchel volatility**
- [X] **yang zhang volatility**

