
from rest_framework.permissions import BasePermission
from .models import UserProfile

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    """

    def has_permission(self, request, view):
        userprofile = UserProfile.objects.get(user=request.user)
        print(userprofile.role,"===================")
        return userprofile.role in ['admin', 'ADMIN']
    
class IsSuperAdminUser(BasePermission):
    """
    Custom permission to only allow super admin users to access certain views.
    """

    def has_permission(self, request, view):
        userprofile = UserProfile.objects.get(user=request.user)
        print(userprofile.role,"===================")

        return userprofile.role in ['SUPER_ADMIN', 'super_admin']

class IsAdminOrSuperAdminUser(BasePermission):
    """
    Custom permission to only allow admin or super admin users to access certain views.
    """

    def has_permission(self, request, view):
        userprofile = UserProfile.objects.get(user=request.user)
        print(userprofile.role,"===================")

        return userprofile.role in ['SUPER_ADMIN', 'super_admin', 'admin', 'ADMIN']
    
