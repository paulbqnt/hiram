//
// Created by zalman on 8/28/24.
//

#ifndef HIRAM_DERIVATIVE_H
#define HIRAM_DERIVATIVE_H


class Derivative {
public:
    virtual double payoff(double underlyingPrice) const = 0;
    virtual ~Derivative() = default;

};


#endif //HIRAM_DERIVATIVE_H
