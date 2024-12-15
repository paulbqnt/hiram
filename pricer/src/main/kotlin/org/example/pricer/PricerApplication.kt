package org.example.pricer

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class PricerApplication

fun main(args: Array<String>) {
    runApplication<PricerApplication>(*args)
}
