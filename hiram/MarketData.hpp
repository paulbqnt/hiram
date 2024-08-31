#ifndef MARKETDATA_HPP
#define MARKETDATA_HPP


class MarketData {
public:
    MarketData(double r, double vol, double s);
    ~MarketData();

    double getRiskFreeRate() const;
    double getVolatility() const;
    double getSpot() const;

    void setRiskFreeRate(double& r);
    void setVolatility(double& vol);
    void setSpot(double& s);

private:
    double volatility;
    double spot;    
    double riskFreeRate;

};

#endif // MARKETDATA_HPP