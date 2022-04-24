from rest_framework import permissions
from character.models import Character

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class HasChampionAlready(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                has_created = Character.objects.filter(created_by=request.user.id)
            except Character.DoesNotExist:
                has_created = None
            if has_created:
                return False
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated):
            return True
        return False

class IsOwnerObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.created_by == request.user
        return True