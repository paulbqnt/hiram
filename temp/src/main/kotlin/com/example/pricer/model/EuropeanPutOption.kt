package com.example.pricer.model

import com.example.pricer.dto.MarketDataRequest
import com.example.pricer.model.MarketData
import com.example.pricer.model.Option
import com.example.pricer.dto.OptionType
import com.example.pricer.pricingmodel.PricingModel

class EuropeanPutOption(override val strikePrice: Double, override val maturity: Double) : Option {
    override val type = OptionType.PUT

    // Implement the price method correctly to accept MarketDataRequest
    override fun price(model: PricingModel, marketData: MarketData): Double {
        // Convert MarketDataRequest to MarketData if necessary
        val marketDataConverted = MarketData(
            underlyingPrice = marketData.underlyingPrice,
            volatility = marketData.volatility,
            riskFreeRate = marketData.riskFreeRate,
            dividendYield = marketData.dividendYield
        )
        // Call the calculatePrice method from the PricingModel (e.g., Black-Scholes or Monte Carlo)
        return model.calculatePrice(this, marketDataConverted)
    }

    // Payoff function for European Put Option: max(strikePrice - underlyingPrice, 0)
    override fun payoff(underlyingPrice: Double): Double {
        return maxOf(strikePrice - underlyingPrice, 0.0)
    }
}