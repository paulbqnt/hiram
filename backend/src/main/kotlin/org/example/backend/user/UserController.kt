package org.example.backend.user

import org.springframework.beans.factory.annotation.Value
import org.springframework.web.bind.annotation.*

data class ViewUser(
    val id: Int,
    val name: String
)

data class CreateUser(
    val name: String
)

data class User(
    val name: String
)



@RestController
@RequestMapping("/users")
class UserController {

    @GetMapping("/")
    fun getAll(): Iterable<ViewUser> =
        listOf(ViewUser(1, "John Doe"))

    @GetMapping("/hello")
    fun hello(): User = User("John Doe")


    @PostMapping("/")
    fun create(@RequestBody request: CreateUser): ViewUser =
        ViewUser(id=2, name=request.name)

}