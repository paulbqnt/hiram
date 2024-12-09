package com.example.pricer.model

data class PricingContext(
    val spot: Double,
    val strike: Double,
    val volatility: Double,
    val riskFreeRate: Double,
    val maturity: Double
)
