package com.example.pricer.model

import com.example.pricer.dto.MarketDataRequest
import com.example.pricer.model.MarketData
import com.example.pricer.model.Option
import com.example.pricer.dto.OptionType
import com.example.pricer.pricingmodel.PricingModel

class EuropeanCallOption(override val strikePrice: Double, override val maturity: Double) : Option {
    override val type = OptionType.CALL

    // Implement the price method correctly to accept MarketDataRequest
    override fun price(model: PricingModel, marketData: MarketData): Double {
        // Call the calculatePrice method from the PricingModel (e.g., Black-Scholes or Monte Carlo)
        val marketDataConverted = MarketData(
            underlyingPrice = marketData.underlyingPrice,
            volatility = marketData.volatility,
            riskFreeRate = marketData.riskFreeRate,
            dividendYield = marketData.dividendYield
        )
        return model.calculatePrice(this, marketDataConverted)
    }

    override fun payoff(underlyingPrice: Double): Double {
        return maxOf(underlyingPrice - strikePrice, 0.0)
    }
}