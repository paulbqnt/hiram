from facade import OptionFacade
from market_data import MarketData

from payoff import VanillaPayoff, StrategyPayoff, call_payoff, put_payoff, strangle_payoff, straddle_payoff, bull_spread_payoff, bear_spread_payoff, butterfly_spread_payoff
from engine import BlackScholesPricingEngine, BinomialPricingEngine, BlackScholesPricer, AmericanBinomialPricer, EuropeanBinomialPricer


if __name__ == "__main__":

    # CALL / PUT
    data = MarketData(spot=100, rate=0.05, volatility=.35, dividend=0)

    call = VanillaPayoff(expiry=.2, strike=100, payoff=call_payoff)
    put = VanillaPayoff(expiry=.2, strike=100, payoff=put_payoff)

    BS_engine_call = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_engine_put = BlackScholesPricingEngine("put", BlackScholesPricer)

    BS_call = OptionFacade(call, BS_engine_call, data)
    BS_put = OptionFacade(put, BS_engine_put, data)

    print(f"call: {BS_call.price()}")
    print(f"put: {BS_put.price()}")

    # STRADDLE
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    straddle = StrategyPayoff(expiry=.2, strike=85, payoff=straddle_payoff, strike_2=110)
    BS_engine_straddle = BlackScholesPricingEngine("straddle", BlackScholesPricer)
    #print(BS_engine_straddle)
    BS_straddle = OptionFacade(straddle, BS_engine_straddle, data)
    print(f"straddle: {BS_straddle.price()}")

    # STRANGLE
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    strangle = StrategyPayoff(expiry=.2, strike=85, payoff=strangle_payoff, strike_2=110)
    BS_engine_strangle = BlackScholesPricingEngine("strangle", BlackScholesPricer)
    #print(BS_engine_strangle)
    BS_strangle = OptionFacade(strangle, BS_engine_strangle, data)
    print(f"strangle: {BS_strangle.price()}")

    #STOCK
    # from stock import Stock
    # aapl = Stock(ticker='AAPL')
    # print(aapl.hist)
    # print(aapl.parkinson_historic_volatility())
    # print(aapl.garman_klass_volatility())
    # print(aapl.rogers_satchel_volatility())
    # print(aapl.yang_zhang_volatility())

    # STRADDLE
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    straddle = StrategyPayoff(expiry=.2, strike=100, payoff=straddle_payoff)
    BS_engine_straddle = BlackScholesPricingEngine("straddle", BlackScholesPricer)
    #print(BS_engine_straddle)
    BS_straddle = OptionFacade(straddle, BS_engine_straddle, data)
    print(f"straddle: {BS_straddle.price()}")

    # STRANGLE
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    strangle = StrategyPayoff(expiry=.2, strike=85, payoff=strangle_payoff, strike_2=110)
    BS_engine_strangle = BlackScholesPricingEngine("strangle", BlackScholesPricer)
    #print(BS_engine_strangle)
    BS_strangle = OptionFacade(strangle, BS_engine_strangle, data)
    print(f"strangle: {BS_strangle.price()}")

    # BULL CALL SPREAD
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    bull_spread = StrategyPayoff(expiry=.2, strike=95, payoff=bull_spread_payoff, strike_2=105)
    BS_engine_bull_spread = BlackScholesPricingEngine("bull_spread", BlackScholesPricer)
    #print(BS_engine_bull_spread)
    BS_bull_spread = OptionFacade(bull_spread, BS_engine_bull_spread, data)
    print(f"bull spread: {BS_bull_spread.price()}")

    # Bear SPREAD
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    bear_spread = StrategyPayoff(expiry=.2, strike=95, payoff=bear_spread_payoff, strike_2=105)
    BS_engine_bear_spread = BlackScholesPricingEngine("bear_spread", BlackScholesPricer)
    #print(BS_engine_bear_spread)
    BS_bear_spread = OptionFacade(bear_spread, BS_engine_bear_spread, data)
    print(f"bear spread: {BS_bear_spread.price()}")

    # Butterfly Spread
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    butterfly_spread = StrategyPayoff(expiry=.2, strike=90, payoff=butterfly_spread_payoff, strike_2=100, strike_3=110)
    BS_engine_butterfly_spread = BlackScholesPricingEngine("butterfly_spread", BlackScholesPricer)
    #print(BS_engine_butterfly_spread)
    BS_butterfly_spread = OptionFacade(butterfly_spread, BS_engine_butterfly_spread, data)
    print(f"butterfly spread: {BS_butterfly_spread.price()}")

    # Strip
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    strip_spread = StrategyPayoff(expiry=.2, strike=100, payoff=butterfly_spread_payoff)
    BS_engine_strip = BlackScholesPricingEngine("strip", BlackScholesPricer)
    #print(BS_engine_butterfly_spread)
    BS_strip = OptionFacade(strip_spread, BS_engine_strip, data)
    print(f"strip: {BS_strip.price()}")

    # Strap
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    strap_spread = StrategyPayoff(expiry=.2, strike=100, payoff=butterfly_spread_payoff)
    BS_engine_strap = BlackScholesPricingEngine("strap", BlackScholesPricer)
    #print(BS_engine_butterfly_spread)
    BS_strap = OptionFacade(strap_spread, BS_engine_strap, data)
    print(f"strap: {BS_strap.price()}")

    # Calendar spread
    data = MarketData(spot=100, rate=0.05, volatility=.3, dividend=0)
    calendar_spread = StrategyPayoff(expiry=.19, strike=100, payoff=butterfly_spread_payoff, expiry_2=.25)
    BS_engine_calendar_spread = BlackScholesPricingEngine("calendar_spread", BlackScholesPricer)
    #print(BS_engine_butterfly_spread)
    BS_calendar_spread = OptionFacade(calendar_spread, BS_engine_calendar_spread, data)
    print(f"calendar spread: {BS_calendar_spread.price()}")

    # PLOTS
    from plot import plot_payoff_vanilla, plot_payoff_straddle, plot_payoff_strangle, plot_payoff_bull_spread, plot_payoff_bear_spread, plot_payoff_butterfly_spread, plot_payoff_strip, plot_payoff_strap
    #plot_payoff_vanilla(BS_call, type_plot='black_scholes')
    # plot_payoff_straddle(BS_straddle)
    # plot_payoff_strangle(BS_strangle)
    # plot_payoff_bull_spread(BS_bull_spread)
    # plot_payoff_bear_spread(BS_bear_spread)
    # plot_payoff_butterfly_spread(BS_butterfly_spread)
    # plot_payoff_strip(BS_strip)
    # plot_payoff_strap(BS_strap)










