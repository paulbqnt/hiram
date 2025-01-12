package org.example.backend.controller.article

import org.example.backend.model.Article
import org.example.backend.repository.ArticleRepository
import org.example.backend.service.ArticleService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/article/")
class ArticleController(
    private val articleService: ArticleService
) {

    @GetMapping
    fun listAll(): List<ArticleResponse> =
        articleService.findAll()
            .map { it.toResponse() }

    private fun Article.toResponse(): ArticleResponse =
        ArticleResponse(
            id = this.id,
            title = this.title,
            content = this.content,
        )
}