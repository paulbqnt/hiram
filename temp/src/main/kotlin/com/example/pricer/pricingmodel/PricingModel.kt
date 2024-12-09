package com.example.pricer.pricingmodel

import com.example.pricer.model.MarketData
import com.example.pricer.model.Option


interface PricingModel {
    fun calculatePrice(option: Option, marketData: MarketData): Double
}