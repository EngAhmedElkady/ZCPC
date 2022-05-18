from rest_framework import permissions
from modules.communnity.models import Communnity  
from modules.round.models import Round


class Community_Permission:
    """this is community permission :
            0- all users have permision to view the community 
            1- if you in community team you will have permission to update 
            2- if you owner you will have permission to update 
            
        all functions in this class take a object
    """
    @staticmethod
    def is_in_community_team(user, community):
        "take user and community"
        team = community.team.all()
        flag = False
        for member in team:
            if user == member.user:
                flag = True
                break
        return flag

    @staticmethod
    def is_teamleader_or_vise(user,community):
        "take user and community"
        team = community.team.all()
        flag = False
        for member in team:
            if user == member.user and (member.role == 'Team Leader' or member.role == "Vise"):
                flag = True
                break
        return flag

    @staticmethod
    def is_in_level_student(user, level):
        "take user and level"
        students = level.levelstudent.all()
        flag = False
        print(students)
        for student in students:
            if user == student.user:
                flag = True
                break
        return flag

    @staticmethod
    def is_in_level_team(user, level):
        "take user ans level"
        team = level.levelteam.all()
        flag = False
        for member in team:
            if user == member.user:
                flag = True
                break
        return flag

    @staticmethod
    def is_owner(user_f,user_s):
        return user_f==user_s