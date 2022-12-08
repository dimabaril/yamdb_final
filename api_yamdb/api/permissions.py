from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission for admin and GET method only."""

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAdmin(permissions.BasePermission):
    """Permission for admin only."""

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAuthorOrAdministratorOrReadOnly(permissions.BasePermission):
    """Permission for author or admin or GET method only."""

    def has_permission(self, request, view):

        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_anonymous
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
