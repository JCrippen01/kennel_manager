from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsStaff(permissions.BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "staff"


class IsCustomer(permissions.BasePermission):
    """
    Allows access only to customer users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"
