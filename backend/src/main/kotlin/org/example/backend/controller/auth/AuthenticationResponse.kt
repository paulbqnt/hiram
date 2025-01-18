package org.example.backend.controller.auth

data class AuthenticationResponse(
    val accessToken: String,
    val refreshToken: String,
)