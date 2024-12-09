package com.example.pricer.factory

import com.example.pricer.model.EuropeanCallOption
import com.example.pricer.model.EuropeanPutOption
import com.example.pricer.factory.OptionFactory
import com.example.pricer.model.Option

class EuropeanOptionFactory : OptionFactory {
    override fun createCallOption(strikePrice: Double, maturity: Double): Option {
        return EuropeanCallOption(strikePrice, maturity)
    }

    override fun createPutOption(strikePrice: Double, maturity: Double): Option {
        return EuropeanPutOption(strikePrice, maturity)
    }
}