package com.example.pricer.dto

data class OptionRequest(
    val type: OptionType,
    val strikePrice: Double,
    val maturity: Double,
    val model: String
)
