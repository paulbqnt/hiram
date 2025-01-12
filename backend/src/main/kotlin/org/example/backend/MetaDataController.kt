package org.example.backend

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController


@RestController
@RequestMapping("/api/metadata")
class MetaDataController {

    @GetMapping("/derivative-types")
    fun getDerivativeTypes(): List<String> {
        return Constants.DERIVATIVE_TYPES
    }

//    @GetMapping("/pricing-models")
//    fun getPricingModels(): List<String> {
//        return Constants.PRICING_MODEL
//    }
}