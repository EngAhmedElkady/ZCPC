from rest_framework import permissions
from modules.communnity.models import Team


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            ok = False
            for i in Team.objecs.all():
                if request.user == i.user_id or i.role == 'leader':
                    ok = True
                
        return ok