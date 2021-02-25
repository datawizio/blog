from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account import serializers as account_serializers
from . import models as article_models


User = get_user_model()


class CommentSerializer(ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=article_models.Post.objects.active(),
        source="post"
    )

    class Meta:
        model = article_models.Comment
        fields = ("id", "post_id", "author", "body",)


class PostListSerializer(ModelSerializer):
    author = account_serializers.UserSerializer(read_only=True)

    class Meta:
        model = article_models.Post
        fields = ("id", "slug", "title", "created", "author")


class PostSerializer(PostListSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        source="author",
    )
    comments = CommentSerializer(many=True, read_only=True)
    slug = serializers.SlugField(required=True)

    class Meta:
        model = article_models.Post
        fields = (
            "id",
            "slug",
            "title",
            "body",
            "active",
            "created",
            "updated",
            "author_id",
            "author",
            "comments",
        )
