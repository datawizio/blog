from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

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
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default="draft", choices=STATUS, max_length=50)

    objects = PostManager()

    class Meta:
        default_related_name = "posts"
        ordering = ("created",)

    def __str__(self) -> str:
        return self.title

    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    session_key = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("post", "session_key"),)
