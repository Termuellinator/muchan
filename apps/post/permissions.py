from rest_framework import permissions


class AuthorSuperOrReadOnly(permissions.BasePermission):
    """Allows only the author or a superuser to modify.
    SAFE_METHODS are allowed for authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.id == obj.user_id.id:
            return True

        return False


class IsAuthenticatedCreateOrSuperDeleteOrReadOnly(permissions.BasePermission):
    """Allows authenticated users to create, superusers to modify and delete.
    Unauthenticated users can only use SAFE_METHODS.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True

            if request.method in ("DELETE", "PUT", "PATCH"):
                return False

            return True

        return False
