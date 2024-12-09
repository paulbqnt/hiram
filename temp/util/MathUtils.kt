package com.example.pricer.util
import org.apache.commons.math3.special.Erf
import kotlin.math.*

fun cumulativeNormalDistribution(x: Double): Double {
    return 0.5 * (1 + Erf.erf(x / sqrt(2.0)))
}