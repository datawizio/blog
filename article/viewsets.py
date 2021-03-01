from rest_framework_extensions.mixins import NestedViewSetMixin

from core.viewsets import BaseModelViewSet

from . import serializers as article_serializers
from . import models as article_models


class PostModelViewSet(BaseModelViewSet):
    queryset = article_models.Post.objects.all().prefetch_related("comments", "author")
    serializer_class = article_serializers.PostSerializer
    serializer_classes = {
        "list": article_serializers.PostListSerializer,
    }


class CommentModelViewSet(NestedViewSetMixin, BaseModelViewSet):
    queryset = article_models.Comment.objects.all()
    serializer_class = article_serializers.CommentSerializer

    def get_serializer(self, *args, **kwargs):
        if kwargs.get("data"):
            kwargs["data"].update(self.get_parents_query_dict())
        return super(CommentModelViewSet, self).get_serializer(*args, **kwargs)

