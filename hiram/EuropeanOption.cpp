#include "EuropeanOption.hpp"

// Constructor for EuropeanOption calling the base class constructor
EuropeanOption::EuropeanOption(double maturity, const Payoff& payoff)
    : Option(maturity, payoff) {}

// Destructor for EuropeanOption
EuropeanOption::~EuropeanOption() {}

// Additional methods specific to EuropeanOption could be implemented here