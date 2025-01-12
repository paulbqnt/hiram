package org.example.backend.repository

import org.example.backend.model.Role
import org.example.backend.model.User
import org.springframework.stereotype.Repository
import java.util.*

@Repository
class UserRepository {

    private val users = mutableListOf<User>(
        User(
            id = UUID.randomUUID(),
            email = "email-1@gmail.com",
            password = "pass1",
            role = Role.USER
        ),
        User(
            id = UUID.randomUUID(),
            email = "email-2@gmail.com",
            password = "pass2",
            role = Role.USER
        ),
        User(
            id = UUID.randomUUID(),
            email = "email-3@gmail.com",
            password = "pass3",
            role = Role.ADMIN
        ),
    )

    fun save(user: User): Boolean =
        users.add(user)

    fun findByEmail(email: String): User? =
        users
            .firstOrNull { it.email == email }

    fun findAll(): List<User> =
        users

    fun findByUUID(uuid: UUID): User? =
        users
            .firstOrNull { it.id == uuid }

    fun deleteByUUID(uuid: UUID): Boolean {
        val foundUser = findByUUID(uuid)

        return foundUser?.let {
            users.remove(it)
        } ?: false
    }


}