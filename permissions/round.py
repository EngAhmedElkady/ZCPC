from rest_framework import permissions
from modules.communnity.models import Communnity,Team

class IsInCommunnityTeamOrNot(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            communnity=Communnity.objects.get(id=obj.communnity_id)
            team=communnity.team.all();
            flag=False
            for member in team:
                if obj.user_id==member.user_id:
                    flag=True
                    break
            return flag