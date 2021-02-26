from django.db import models
from django.contrib.auth import get_user_model

from .managers import PostManager

User = get_user_model()

STATUS = (
    ("draft", "Draft"),
    ("publish", "Publish"),
)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default="draft", choices=STATUS, max_length=50)

    objects = PostManager()

    class Meta:
        default_related_name = "posts"
        ordering = ("created",)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_on",)
