from rest_framework.permissions import BasePermission

from .models import AccountOwner


class IsBusinessOwner(BasePermission):
    """
    Allows access only to "Business Owner" users.
    """

    def has_permission(self, request, view):
        return request.user and \
            request.user.category == AccountOwner.BUSINESS_OWNER


class IsGeneralUser(BasePermission):
    """
    Allows access only to "Business Owner" users.
    """

    def has_permission(self, request, view):
        return request.user and \
            request.user.category == AccountOwner.GENERAL_USER
