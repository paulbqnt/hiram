#ifndef OPTION_HPP
#define OPTION_HPP

#include "Payoff.hpp"

class Option {
public:
    virtual ~Option() {}  // Virtual destructor for proper cleanup of derived objects

    double getMaturity() const;  // Getter for maturity
    const Payoff& getPayoff() const;  // Getter for payoff

protected:
    Option(double maturity, const Payoff& payoff);  // Protected constructor to be called by derived classes

private:
    double maturity;
    const Payoff* payoff;  // Pointer to handle polymorphic behavior for different payoff types
};

#endif // OPTION_HPP
