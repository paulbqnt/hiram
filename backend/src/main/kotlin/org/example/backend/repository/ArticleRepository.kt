package org.example.backend.repository

import org.example.backend.model.Article
import org.springframework.stereotype.Repository
import java.util.*
import java.util.UUID.*

@Repository
class ArticleRepository {

    private val articles = listOf(
        Article(id = UUID.randomUUID(), title = "Article 1", content = "Content 1"),
        Article(id = UUID.randomUUID(), title = "Article 2", content = "Content 2"),
        Article(id = UUID.randomUUID(), title = "Article 3", content = "Content 3"),
    )

    fun findAll(): List<Article> =
        articles
}