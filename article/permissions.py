from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from article.models import Post


class PostPermission(BasePermission):
    message = "Don`t have access to this post!"

    def has_permission(self, request: Request, view):
        return True

    def has_object_permission(self, request: Request, view, obj: Post):
        if request.method.lower() == "get":
            # Allowed to read only
            return True
        if obj.author == request.user:
            return True
        return False

