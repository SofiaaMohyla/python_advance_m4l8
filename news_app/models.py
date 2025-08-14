from django.conf import settings
from django.db import models

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Чернетка"
        PUBLISHED = "published", "Опубліковано"

    class Priority(models.IntegerChoices):
        LOW = 1, "Низький"
        MEDIUM = 2, "Середній"
        HIGH = 3, "Високий"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
