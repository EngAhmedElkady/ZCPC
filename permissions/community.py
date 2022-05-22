from rest_framework import permissions
from modules.communnity.models import Communnity
from modules.round.models import Round


class IsInCommunnityTeam(permissions.BasePermission):
    """
    if current user in the Communnity team he will has a permission
    to delete and update all future in this community
    """

    def has_object_permission(self, request, view, obj):
        communnity = obj.get_community()
        print(communnity)
        team = communnity.team.all()
        print(team)
        flag = False
        for member in team:
            if request.user == member.user:
                flag = True
                break
        return flag


class IsTeamLeader_OR_VICE(permissions.BasePermission):
    """
    if current user is a teamleader he will has a permission
    to delete and update all future in this community
    """
    print(111)

    def has_object_permission(self, request, view, obj):
        print(IsTeamLeader_OR_VICE)
        communnity = obj.get_community()
        team = communnity.team.all()
        flag = False
        for member in team:
            if request.user == member.user and (member.role == 'Team Leader' or member.role == "Vice"):
                flag = True
                break
        return flag


class IsOwner(permissions.BasePermission):
    print('aaaaaaaaaaa')

    def has_object_permission(self, request, view, obj):
        print("IsOwner")
        return request.user == obj.owner


class IsCurrentUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request.user, obj.user)
        return request.user == obj.user
