from django.db import models
from django.contrib.auth import get_user_model

from .managers import PostManager

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        default_related_name = "posts"
        ordering = ("created", )


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_on", )
