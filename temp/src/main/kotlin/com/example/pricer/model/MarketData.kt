package com.example.pricer.model

data class MarketData(
    val underlyingPrice: Double,
    val volatility: Double,
    val riskFreeRate: Double,
    val dividendYield: Double = 0.0
)