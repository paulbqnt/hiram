package org.example.backend.controller.auth

data class AuthenticationRequest(
    val email: String,
    val password: String,
)
