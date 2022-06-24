# help function
from modules.community.models import Community  
from modules.level.models import Level

class Community_Function:
    """this is community permission :
            0- all users have permision to view the community 
            1- if you in community team you will have permission to update 
            2- if you owner you will have permission to update 
            
        all functions in this class take a object
    """
    @staticmethod
    def is_in_community_team(user, obj):
        "take user and community"
        community = obj.get_community()
        team = community.team.all()
        flag = False
        for member in team:
            if user == member.user:
                flag = True
                break
        return flag

    @staticmethod
    def is_teamleader_or_vise(user,obj):
        "take user and community"
        community = obj.get_community()
        team = community.team.all()
        flag = False
        for member in team:
            if user == member.user and (member.role == 'Team Leader' or member.role == "Vice"):
                flag = True
                break
        return flag

    @staticmethod
    def is_in_level_student(user, level):
        "take user and level"
        students = level.students.all()
        flag = False
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
        # print( user_f.username,user_s.username)
        return user_f.username==user_s.username
