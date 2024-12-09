package com.example.pricer.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import com.example.pricer.pricingmodel.BlackScholesModel
import com.example.pricer.pricingmodel.MonteCarloModel
import com.example.pricer.pricingmodel.PricingModel

@Configuration
class OptionPricingConfig {

    @Bean
    fun blackScholesModel(): BlackScholesModel {
        return BlackScholesModel()
    }

    @Bean
    fun monteCarloModel(): MonteCarloModel {
        return MonteCarloModel()
    }
}