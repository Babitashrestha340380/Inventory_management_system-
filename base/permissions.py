from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    """
    Full access if user is superuser or staff.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Admin/staff gets full access


class IsInventoryManager(BasePermission):
    """
    Only InventoryManager group can access.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True  # Admin gets full access
        return request.user.groups.filter(name='InventoryManager').exists()


class IsSales(BasePermission):
    """
    Only Sales group can access.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True  # Admin gets full access
        return request.user.groups.filter(name='Sales').exists()


class ReadOnly(BasePermission):
    """
    Read-only access for authenticated users.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True  # Admin gets full access
        return request.method in SAFE_METHODS
