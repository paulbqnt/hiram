
#ifndef HIRAM_MARKETDATA_H
#define HIRAM_MARKETDATA_H


class MarketData {
    double riskFreeRate;
    double volatility;

public:
    MarketData(double r, double vol);
    double getRiskFreeRate() const;
    double getVolatility() const;
};


#endif //HIRAM_MARKETDATA_H
