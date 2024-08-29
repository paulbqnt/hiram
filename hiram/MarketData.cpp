#include "MarketData.h"

// Constructor
MarketData::MarketData(double r, double vol, double s) : riskFreeRate(r), volatility(vol), spot(s) {}

double MarketData::getRiskFreeRate() const {
    return riskFreeRate;
}

double MarketData::getVolatility() const {
    return volatility;
}

double MarketData::getSpot() const {
    return spot;
}

void MarketData::setRiskFreeRate(double r) {
    riskFreeRate = r;
}

void MarketData::setVolatility(double vol) {
    volatility = vol;

}

void MarketData::setSpot(double s) {
    spot = s;
}