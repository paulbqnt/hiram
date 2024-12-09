package com.example.pricer.pricingmodel

import com.example.pricer.model.MarketData
import com.example.pricer.model.Option

class MonteCarloModel : PricingModel {
    override fun calculatePrice(option: Option, marketData: MarketData): Double {
        // Implement Monte Carlo pricing logic here
        return 0.0
    }
}