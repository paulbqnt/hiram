
#include "Option.hpp"

// Option class constructor
Option::Option(double maturity, const Payoff& payoff)
    : maturity(maturity), payoff(&payoff) {}  // Initialize maturity and payoff pointer

// Getter for maturity
double Option::getMaturity() const {
    return maturity;
}

// Getter for payoff
const Payoff& Option::getPayoff() const {
    return *payoff;
}
