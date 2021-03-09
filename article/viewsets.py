from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from core.viewsets import BaseModelViewSet, BaseReadOnlyViewSet

from . import serializers as article_serializers
from . import permissions as article_permissions
from . import models as article_models


class PostModelViewSet(BaseModelViewSet):
    queryset = article_models.Post.objects.all().prefetch_related("comments", "author")
    permission_classes = [IsAuthenticatedOrReadOnly, article_permissions.PostPermission]
    serializer_class = article_serializers.PostSerializer
    serializer_classes = {
        "list": article_serializers.PostListSerializer,
    }

    def get_queryset(self):
        queryset = super(PostModelViewSet, self).get_queryset()
        queryset = queryset.annotate(likes_count=Count("likes"), comments_count=Count("comments"))
        return queryset

    @action(methods=["post"], detail=True, url_path="like", url_name="like", permission_classes=[AllowAny])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        session_key = request.data.get("session_key", request.session.session_key or request.META.get('REMOTE_ADDR'))

        if session_key is not None:
            if liked_post := post.likes.filter(session_key=session_key).first():
                liked_post.delete()
            else:
                article_models.Like.objects.create(session_key=session_key, post=post)

        return Response({"likes": post.likes.count()})

    @action(methods=["GET"], detail=False, url_path="top_by_likes", url_name="top_by_likes")
    def top_by_likes(self, request, *args, **kwargs):
        top = int(request.query_params.get("top", 10))
        queryset = self.get_queryset().order_by("-like_count")[:top]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="top_by_comments", url_name="top_by_comments")
    def top_by_comments(self, request, *args, **kwargs):
        top = int(request.query_params.get("top", 10))
        queryset = self.get_queryset().order_by("-comments_count")[:top]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentModelViewSet(NestedViewSetMixin, BaseReadOnlyViewSet, CreateModelMixin):
    queryset = article_models.Comment.objects.all()
    serializer_class = article_serializers.CommentSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        if kwargs.get("data"):
            kwargs["data"].update(self.get_parents_query_dict())
        return super(CommentModelViewSet, self).get_serializer(*args, **kwargs)

