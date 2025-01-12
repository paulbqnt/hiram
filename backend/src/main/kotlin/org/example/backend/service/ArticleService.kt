package org.example.backend.service

import org.example.backend.model.Article
import org.example.backend.repository.ArticleRepository
import org.springframework.stereotype.Service

@Service
class ArticleService(
    private val articleRepository: ArticleRepository
) {
    fun findAll(): List<Article> =
        articleRepository.findAll()
}