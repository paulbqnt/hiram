#include "PayoffPut.hpp"
#include <algorithm>

PayoffPut::PayoffPut(double strike) : strike(strike) {}

PayoffPut::~PayoffPut() {}

double PayoffPut::operator()(double spot) const {
    return std::max(spot - strike, 0.0);
}