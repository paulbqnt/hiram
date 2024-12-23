package org.example.backend

import jakarta.persistence.EntityManager
import jakarta.persistence.PersistenceContext
import org.apache.logging.log4j.LogManager
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/backend")
class HelloController {

    val logger = LogManager.getLogger(HelloController::class.java)

    @PersistenceContext
    lateinit var entityManager: EntityManager

    @GetMapping("/hello")
    fun hello(): String {
        logger.trace("TRACE line")
        logger.debug("DEBUG line")
        logger.info("info line")
        logger.warn("warn line")
        logger.error("error line")

        logger.info("INFO {} {}", 1, "abc")
        try {
            val x = 1 / 0
        } catch (e: Throwable) {
            logger.error("ERR failed to compute x", e)
        }

        return "Hello World!"
    }

    @GetMapping("/db-check")
    fun dbCheck(): String {
        return try {
            // Execute a simple query to check the database connection
            entityManager.createNativeQuery("SELECT 1").singleResult
            "Database connection is working"
        } catch (e: Exception) {
            logger.error("Database connection check failed", e)
            "Database connection check failed: ${e.message}"
        }
    }
}