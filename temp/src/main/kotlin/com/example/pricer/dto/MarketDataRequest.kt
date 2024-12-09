package com.example.pricer.dto

data class MarketDataRequest(
    val underlyingPrice: Double,
    val volatility: Double,
    val riskFreeRate: Double,
    val dividendYield: Double = 0.0
)