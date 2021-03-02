from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Like, Post, Comment

# Register your models here.


class CommentAdminModelInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    inlines = [CommentAdminModelInline]
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "slug", "status", "created")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related("comments")


@admin.register(Like)
class LikeAdminModel(admin.ModelAdmin):
    list_display = ("post", "session_key", "created")
