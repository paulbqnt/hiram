#include <iostream>

#include "MarketData.hpp"
#include "Option.hpp"
#include "PayoffCall.hpp"
#include "PayoffPut.hpp"
#include "EuropeanOption.hpp"
#include "BlackScholesModel.hpp"


int main()
{
	MarketData marketData(0.05, 0.25, 100);

	PayoffCall payoffCall(100.0);
	PayoffPut payoffPut(100.0);

	EuropeanOption callOption(1.0, payoffCall);
	EuropeanOption putOption(1.0, payoffPut);

	BlackScholesModel bsModel(marketData);
	BlackScholesModel bsModel2(marketData);

	double callPrice = bsModel.price(callOption, marketData.getSpot());
	double putPrice = bsModel.price(callOption, marketData.getSpot());
	
	std::cout << "call price: " << callPrice << std::endl;
	std::cout << "put price: " << putPrice << std::endl;

	return 0;
}




//MarketData DONE
//EuropeanCallPayoff DONE
//EuropeanOption(EuropeanCallPayoff) DONE
//BlackScholesModel
//double bsPrice = BlackScholesModel.price(europeanOption, marketData)