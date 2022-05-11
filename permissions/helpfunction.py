# help function
from modules.communnity.models import Communnity
from modules.level.models import Level
def incommunityteam(user, id):
    communnity = Communnity.objects.get(id=id)
    team = communnity.team.all()
    flag = False
    for member in team:
        if user == member.user_id.id:
            flag = True
            break
    return flag


def isteamleader(user, id):
    communnity = Communnity.objects.get(id=id)
    team = communnity.team.all()
    flag = False
    for member in team:
        if int(user) == member.user_id.id and (member.role == 'Team Leader' or member.role == "Vise"):
            flag = True
            break
    return flag


def isinlevelstudent(user, id):
    level = Level.objects.get(id=id)
    students = level.levelstudent.all()
    flag = False
    print(students)
    for student in students:
        if int(user) == student.user.id:
            flag = True
            break
    return flag


def isinlevelteam(user_id, id):
    round = Level.objects.get(id=id)
    team = round.levelteam.all()
    flag = False
    for member in team:
        if int(user_id) == member.user.id:
            flag = True
            break
    return flag
