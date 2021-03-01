from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from core.mixins import GenericViewSetMixin


class BaseModelViewSet(ModelViewSet, GenericViewSetMixin):
    filter_backends = [SearchFilter, OrderingFilter]


class BaseReadOnlyViewSet(ReadOnlyModelViewSet, GenericViewSetMixin):
    filter_backends = [SearchFilter, OrderingFilter]

