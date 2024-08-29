#include "MarketData.h"

// Constructor
MarketData::MarketData(double r, double vol) : riskFreeRate(r), volatility(vol) {}

double MarketData::getRiskFreeRate() const {
    return riskFreeRate;
}

double MarketData::getVolatility() const {
    return volatility;
}