from rest_framework import permissions
from modules.communnity.models import Communnity,Team

class IsInCommunnityTeam(permissions.BasePermission):
    """
    if current user in the Communnity team he will has a permission
    to delete and update all future in this community
    
    """

    def has_object_permission(self, request, view, obj):
        
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            communnity=Communnity.objects.get(id=obj.communnity.id)
            team=communnity.team.all();
            flag=False
            for member in team:
                if request.user==member.user_id:
                    flag=True
                    break
            return flag