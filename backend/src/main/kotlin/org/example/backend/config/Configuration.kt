package org.example.backend.config

import org.springframework.boot.context.properties.EnableConfigurationProperties

@Configuration
@EnableConfigurationProperties(JwtProperties::class)
class Configuration {

}