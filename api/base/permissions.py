from rest_framework import permissions


class SportoAdminPermission(permissions.BasePermission):
    """
        Global permission check for sportomatics admins.
    """
    def has_permission(self, request, view):
        return request.user.is_staff