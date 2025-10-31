
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin'| 'ADMIN'
    
class IsSuperAdminUser(BasePermission):
    """
    Custom permission to only allow super admin users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'super_admin'| 'SUPER_ADMIN'
    
