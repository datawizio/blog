from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.viewsets import BaseModelViewSet
from article import serializers as article_serializer

from . import serializers as account_serializers

User = get_user_model()


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = account_serializers.UserSerializer
    serializer_classes = {
        "posts": article_serializer.PostListSerializer,
    }
    ordering = ["id"]

    @action(methods=["get"], detail=True, url_name="posts", url_path="posts")
    def posts(self, request, *args, **kwargs) -> Response:
        user = self.get_object()
        posts = user.posts.active()
        serializer = self.get_serializer(instance=posts, many=True)
        return Response(
            {
                "count": posts.count(),
                "results": serializer.data,
            }
        )

    @action(
        methods=["get"],
        detail=False,
        url_name="current",
        url_path="current",
        permission_classes=[IsAuthenticated]
    )
    def current(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
