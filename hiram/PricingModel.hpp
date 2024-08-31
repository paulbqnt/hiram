#ifndef PRICINGMODEL_H
#define PRICINGMODEL_H

#include "Option.hpp"
#include "MarketData.hpp"

class PricingModel {
public:
	virtual ~PricingModel() {}
	virtual double price(const Option& option, double spot) const = 0;  // Pure virtual function

};

#endif