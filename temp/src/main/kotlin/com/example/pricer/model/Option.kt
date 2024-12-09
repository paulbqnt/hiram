package com.example.pricer.model

import com.example.pricer.dto.MarketDataRequest
import com.example.pricer.dto.OptionType
import com.example.pricer.pricingmodel.PricingModel


interface Option {
    val type: OptionType
    val strikePrice: Double
    val maturity: Double

    // Update the price method to accept MarketDataRequest
    fun price(model: PricingModel, marketData: MarketData): Double
    fun payoff(underlyingPrice: Double): Double
}
