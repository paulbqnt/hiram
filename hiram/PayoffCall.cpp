#include "PayoffCall.hpp"
#include <algorithm>

PayoffCall::PayoffCall(double strike) : strike(strike) {}

PayoffCall::~PayoffCall() {}

double PayoffCall::operator()(double spot) const {
    return std::max(spot - strike, 0.0);
}