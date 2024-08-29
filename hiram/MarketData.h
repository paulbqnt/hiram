
#ifndef HIRAM_MARKETDATA_H
#define HIRAM_MARKETDATA_H


class MarketData {
    double riskFreeRate;
    double volatility;
    double spot;

public:
    double getRiskFreeRate() const;
    double getVolatility() const;
    double getSpot() const;

    MarketData(double r, double vol, double s);

    void setRiskFreeRate(double r);
    void setVolatility(double vol);
    void setSpot(double s);
};


#endif //HIRAM_MARKETDATA_H
