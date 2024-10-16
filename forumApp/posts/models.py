from django.db import models

from forumApp.posts.choices import LanguageChoice
from forumApp.posts.validators import BadLanguageValidator


class Post(models.Model):
    title = models.CharField(
        max_length=100,
    )

    content = models.TextField(
        validators=(
            BadLanguageValidator(),
        )
    )

    author = models.CharField(
        max_length=30
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    languages = models.CharField(
        max_length=20,
        choices=LanguageChoice.choices,
        default=LanguageChoice.OTHER,
    )


class Comment(models.Model):
    content = models.TextField(
        max_length=300,
        validators=(
            BadLanguageValidator(),
        )
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content

