from rest_framework import permissions
from modules.community.models import Community
from modules.round.models import Round


class IsInCommunnityTeam(permissions.BasePermission):
    """
    if current user in the Communnity team he will has a permission
    to delete and update all future in this community
    """

    massage = "you are not in the team"

    def has_object_permission(self, request, view, obj):
        community = obj.get_community()
        team = community.team.all()
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
        community = obj.get_community()
        team = community.team.all()
        flag = False
        for member in team:
            if request.user == member.user and (member.role == 'Team Leader' or member.role == "Vice"):
                flag = True
                break
        return flag


class IsOwner(permissions.BasePermission):
    massage = "you are not owner"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsCurrentUser(permissions.BasePermission):
    massage = "you are not the current user"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsInLevelTeam(permissions.BasePermission):
    massage = "you are not in the level team"

    def has_object_permission(self, request, view, obj):

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

        students = obj.levelstudent.all()
        flag = False
        print(students)
        for student in students:
            if request.user == student.user:
                flag = True
                break
        return flag
