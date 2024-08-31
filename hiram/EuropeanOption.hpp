#ifndef EUROPEANOPTION_HPP
#define EUROPEANOPTION_HPP

#include "Option.hpp"

class EuropeanOption : public Option {
public:
    EuropeanOption(double maturity, const Payoff& payoff);  // Constructor
    ~EuropeanOption();

};

#endif