# hiram
Hiram is a free financial library built in  python that can be used for option pricing.

--- 

## How to use it

### Stock

The _Stock_ object is the basic underlying used for option pricing.

```python
from stock import Stock
amzn_stock = Stock(ticker="AMZN")
```


### VanillaOption

The _VanillaOption_ object is used to represent call and put we want to price.


```python
from option import VanillaOption
call = VanillaOption(way="call", k=100, t=1, style="euro")
```

### BlackScholesModel

```python
from option import VanillaOption
from model import BlackScholesModel
call = VanillaOption(way="call", k=100, t=1, style="euro")
bsm = BlackScholesModel(spot=100, r=0.05, sigma=0.3)

# to price the option
call.pricer(bsm)
```


