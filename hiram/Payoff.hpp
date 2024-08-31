#ifndef PAYOFF_HPP
#define PAYOFF_HPP

class Payoff {
public:
    virtual ~Payoff() {}
    virtual double operator()(double spot) const = 0;  // Pure virtual function
};

#endif // PAYOFF_HPP