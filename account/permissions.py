from rest_framework.permissions import BasePermission, IsAuthenticated


class UserPermission(BasePermission):
    allowed_read_only_methods = ("get", )
    allowed_change_methods = ("put", "update", "delete")

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method.lower() in self.allowed_read_only_methods:
            return True
        if request.method.lower() in self.allowed_change_methods:
            # The user can only change the data about himself
            return IsAuthenticated().has_permission(request, view) and (obj is request.user)
        return True
