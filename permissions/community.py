from rest_framework import permissions
from modules.communnity.models import Communnity
from modules.round.models import Round

class IsInCommunnityTeam(permissions.BasePermission):
    """
    if current user in the Communnity team he will has a permission
    to delete and update all future in this community
    
    """

    def has_object_permission(self, request, view, obj):
        
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            round_id = obj.round.id
            round=Round.objects.get(id=round_id);
            community_id=round.communnity.id
            communnity=Communnity.objects.get(id=community_id)
            team=communnity.team.all();
            flag=False
            for member in team:
                if request.user==member.user_id:
                    flag=True
                    break
            return flag
        
class IsTeamLeader(permissions.BasePermission):
    """
    if current user is a teamleader he will has a permission
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
                if request.user==member.user_id and(member.role=='Team Leader' or member.role=="Vise"):
                    flag=True
                    break
            return flag