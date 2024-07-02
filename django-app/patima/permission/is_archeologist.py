from rest_framework import permissions


class IsArcheologist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 2
