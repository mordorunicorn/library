from rest_framework import permissions


class CanPerformWriteAction(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action in ('create', 'update', 'partial_update'):
                return False
        return True
