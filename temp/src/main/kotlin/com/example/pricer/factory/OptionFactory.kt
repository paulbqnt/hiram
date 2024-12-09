package com.example.pricer.factory

import com.example.pricer.model.Option

interface OptionFactory {
    fun createCallOption(strikePrice: Double, maturity: Double): Option
    fun createPutOption(strikePrice: Double, maturity: Double): Option
}