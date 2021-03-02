from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account import serializers as account_serializers
from . import models as article_models

User = get_user_model()


class CommentSerializer(ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=article_models.Post.objects.all(),
        source="post"
    )

    class Meta:
        model = article_models.Comment
        fields = ("id", "post_id", "author", "body",)


class PostListSerializer(ModelSerializer):
    author = account_serializers.UserSerializer(read_only=True)
    likes = serializers.IntegerField(source="likes_count", read_only=True)
    status = serializers.ChoiceField(
        choices=article_models.STATUS,
        default="draft",
        required=False
    )

    class Meta:
        model = article_models.Post
        fields = (
            "id",
            "slug",
            "title",
            "status",
            "created",
            "likes",
            "author",
        )


class PostSerializer(PostListSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        source="author",
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = article_models.Post
        fields = (
            "id",
            "slug",
            "title",
            "body",
            "created",
            "updated",
            "status",
            "likes",
            "author_id",
            "author",
            "comments",
        )
