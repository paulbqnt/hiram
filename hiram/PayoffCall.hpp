#ifndef PAYOFFCALL_HPP
#define PAYOFFCALL_HPP

#include "Payoff.hpp"

class PayoffCall : public Payoff {
public:
    PayoffCall(double strike);  // Constructor
    ~PayoffCall();             // Destructor

    double operator()(double spot) const override;  // Override the pure virtual function

private:
    double strike;  // Strike price for the call option
};

#endif // PAYOFFCALL_HPP

