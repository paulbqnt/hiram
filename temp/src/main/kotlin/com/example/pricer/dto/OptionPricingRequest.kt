package com.example.pricer.dto

data class OptionPricingRequest(
    val underlyingPrice: Double,
    val volatility: Double,
    val riskFreeRate: Double,
    val dividendYield: Double,
    val optionType: String,  // "CALL" or "PUT"
    val modelType: String,   // "BlackScholes" or "MonteCarlo"
    val strikePrice: Double,
    val maturity: Double
)