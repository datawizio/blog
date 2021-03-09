from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from article.models import Post


class PostPermission(BasePermission):
    message = "Don`t have access to this post!"

    def has_permission(self, request: Request, view):
        return True

    def has_object_permission(self, request: Request, view, obj: Post):
        if request.method.upper() in SAFE_METHODS:
            # Allowed to read only
            return True
        if obj.author == request.user:
            return True
        return False

