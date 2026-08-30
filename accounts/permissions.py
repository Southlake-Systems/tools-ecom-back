from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Profile
from .utils import get_role


class IsAdminOrReadOnly(BasePermission):
    """Read for everyone; write only for authenticated users with the 'admin' role."""

    message = "You need an admin role to perform this action."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and get_role(user) == Profile.Role.ADMIN
        )


class IsPanelUser(BasePermission):
    """Any authenticated panel user (admin or viewer)."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
