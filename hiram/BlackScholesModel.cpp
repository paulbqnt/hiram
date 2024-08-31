#include "BlackScholesModel.hpp"
#include <cmath>
#include <stdexcept>


BlackScholesModel::BlackScholesModel(const MarketData& marketData)
    :  marketData(marketData) {}

BlackScholesModel::~BlackScholesModel() {}

double BlackScholesModel::price(const Option& option, double spot) const {
    double riskFreeRate = marketData.getRiskFreeRate();
    double volatility = marketData.getVolatility();
    double maturity = option.getMaturity();
    return riskFreeRate * volatility;

}