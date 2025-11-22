from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS
)


class IsAdminOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return IsAuthenticated().has_permission(request, view)

        return IsAdminUser().has_permission(request, view)
