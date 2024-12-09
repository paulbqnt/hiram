package com.example.pricer.controller

import com.example.pricer.dto.MarketDataRequest
import com.example.pricer.model.EuropeanCallOption
import com.example.pricer.model.EuropeanPutOption
import com.example.pricer.model.MarketData
import com.example.pricer.service.PricerService
import com.example.pricer.model.PricingContext
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController


@RestController
@RequestMapping("/api/options")
class PricerController(
    private val pricerService: PricerService
) {
    @PostMapping("/price")
    fun calculateOptionPrice(
        @RequestBody marketDataRequest: MarketDataRequest,
        @RequestParam optionType: String,  // "CALL" or "PUT"
        @RequestParam modelType: String    // "BlackScholes" or "MonteCarlo"
    ): Double {

        // Create the option based on the input type (CALL/PUT)
        val option = when (optionType) {
            "CALL" -> EuropeanCallOption(strikePrice = 100.0, maturity = 1.0)  // Example strike and maturity
            "PUT" -> EuropeanPutOption(strikePrice = 100.0, maturity = 1.0)
            else -> throw IllegalArgumentException("Invalid option type")
        }

        // Map MarketDataRequest to MarketData model
        val marketData = MarketData(
            underlyingPrice = marketDataRequest.underlyingPrice,
            volatility = marketDataRequest.volatility,
            riskFreeRate = marketDataRequest.riskFreeRate,
            dividendYield = marketDataRequest.dividendYield
        )

        // Calculate the price using the service
        return pricerService.calculatePrice(option, modelType, marketData)
    }
}