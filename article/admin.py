from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Post, Comment

# Register your models here.


class CommentAdminModelInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    inlines = [CommentAdminModelInline]
    pass

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related("comments")
