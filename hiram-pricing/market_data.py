class MarketData(object):
    def __init__(self, spot: float, rate: float, volatility: float, dividend: float):
        self.__spot = spot
        self.__rate = rate
        self.__volatility = volatility
        self.__dividend = dividend

    @property
    def spot(self):
        return self.__spot

    @spot.setter
    def spot(self, new_spot):
        self.__spot = new_spot

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, new_rate):
        self.__rate = new_rate

    @property
    def volatility(self):
        return self.__volatility

    @volatility.setter
    def volatility(self, new_volatility):
        self.__volatility = new_volatility

    @property
    def dividend(self):
        return self.__dividend

    @dividend.setter
    def dividend(self, new_dividend):
        self.__dividend = new_dividend

    def get_data(self):
        return self.__spot, self.__rate, self.__volatility, self.__dividend

    def __repr__(self):
        return f"MarketData({self.__spot},{self.__rate},{self.__volatility},{self.__dividend})"
