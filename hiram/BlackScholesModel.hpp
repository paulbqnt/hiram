#ifndef BLACKSCHOLESMODEL_HPP
#define BLACKSCHOLESMODEL_HPP

#include "PricingModel.hpp"
#include "MarketData.hpp"
#include "Option.hpp"


class BlackScholesModel : public PricingModel {
public:
	BlackScholesModel(const MarketData& marketData);
	~BlackScholesModel();
	double price(const Option& option, double spot) const;



private:
	const MarketData& marketData;

};



#endif