from .models import Profile


def get_role(user):
    """Return the RBAC role string for a user: 'admin' or 'viewer'."""
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return Profile.Role.ADMIN
    profile = getattr(user, "profile", None)
    return profile.role if profile else Profile.Role.VIEWER
