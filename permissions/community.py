from rest_framework import permissions
from modules.communnity.models import Communnity
from modules.round.models import Round


class IsInCommunnityTeam(permissions.BasePermission):
    """
    if current user in the Communnity team he will has a permission
    to delete and update all future in this community
    """

    massage = "you are not in the team"

    def has_object_permission(self, request, view, obj):
        print('IsInCommunnityTeam')
        communnity = obj.get_community()
        team = communnity.team.all()
        print("team:", team)
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
    massage = "you are not team leader or vice"

    def has_object_permission(self, request, view, obj):
        print('IsTeamLeader_OR_VICE')
        communnity = obj.get_community()
        team = communnity.team.all()
        print(team)
        flag = False
        for member in team:
            if request.user == member.user and (member.role == 'Team Leader' or member.role == "Vice"):
                flag = True
                break
        return flag


class IsOwner(permissions.BasePermission):
    massage = "you are not owner"

    def has_object_permission(self, request, view, obj):
        print("IsOwner")
        print(request.user, obj.owner)
        return request.user == obj.owner


class IsCurrentUser(permissions.BasePermission):
    massage = "you are not the current user"

    def has_object_permission(self, request, view, obj):
        print('IsCurrentUser')
        print(request.user, obj.user)
        return request.user == obj.user


class IsInLevelTeam(permissions.BasePermission):
    massage = "you are not in the level team"

    def has_object_permission(self, request, view, obj):
        print('IsInLevelTeam')

        team = obj.levelteam.all()
        flag = False
        for member in team:
            if request.user == member.user:
                flag = True
                break
        return flag


class IsInLevelStudent(permissions.BasePermission):
    massage = "you are not in the level student"

    def has_object_permission(self, request, view, obj):
        print('IsInLevelStudent')

        students = obj.levelstudent.all()
        flag = False
        print(students)
        for student in students:
            if request.user == student.user:
                flag = True
                break
        return flag
