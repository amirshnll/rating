from rest_framework import permissions
from .models import UserTypes


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator


class IsLogginedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.id is not None
            and request.user.id > 0
            and request.user.is_deleted == False
        )


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == UserTypes.AUTHOR
