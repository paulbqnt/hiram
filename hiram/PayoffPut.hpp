#ifndef PAYOFFPUT_HPP
#define PAYOFFPUT_HPP


#include "Payoff.hpp"

class PayoffPut : public Payoff {
public:
    PayoffPut(double strike);  // Constructor
    ~PayoffPut();             // Destructor

    double operator()(double spot) const override;  // Override the pure virtual function

private:
    double strike;  // Strike price for the call option
};

#endif // PAYOFFCALL_HPP