# help function 
from modules.communnity.models import Communnity
from modules.round.models import Round

def incommunityteam(user,id):
    communnity=Communnity.objects.get(id = id)
    team=communnity.team.all();
    flag = False
    for member in team:
        if int(user) == member.user_id.id:
            flag=True
            break
    return flag


def isteamleader(user,id):
    communnity=Communnity.objects.get(id = id)
    team=communnity.team.all();
    flag = False
    for member in team:
        if int(user) == member.user_id.id and (member.role=='Team Leader' or member.role=="Vise"):
            flag=True
            break
    return flag

def isinroundstudent(user,id):
    round = Round.objects.get(id=id)
    students = round.roundstudent.all()
    flag = False
    for student in students:
        if int(user) == student.user.id:
            flag = True
            break
    return flag

def isinroundteam(user_id,id):
    round = Round.objects.get(id=id)
    team = round.roundteam.all()
    flag = False
    for member in team:
        if int(user_id) == member.user.id:
            flag = True
            break
    return flag
