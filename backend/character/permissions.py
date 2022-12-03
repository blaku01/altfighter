from rest_framework import permissions

from character.models import Character

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class DisallowPatch(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            return False
        return True


class DisallowPut(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT":
            return False
        return True


class HasChampionAlready(permissions.BasePermission):
    message = "You have a champion already!"

    def has_permission(self, request, view):
        if request.method == "POST":
            try:
                has_created = Character.objects.filter(created_by=request.user.id)
            except Character.DoesNotExist:
                has_created = None
            if has_created:
                return False
        if (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        ):
            return True
        return False


class IsObjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" or request.method == "PUT":
            return obj.created_by == request.user
        return True
