from rest_framework.permissions import BasePermission

from .models import AccountOwner


class IsBusinessOwner(BasePermission):
    """
    Allows access only to "Business Owner" users.
    """

    def has_permission(self, request, view):
        user = request.user
        return user and \
            getattr(user, 'category', -1) == AccountOwner.BUSINESS_OWNER


class IsGeneralUser(BasePermission):
    """
    Allows access only to "Business Owner" users.
    """

    def has_permission(self, request, view):
        user = request.user
        return user and \
            getattr(user, 'category', -1) == AccountOwner.GENERAL_USER
