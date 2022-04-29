# help function 
from modules.communnity.models import Communnity

def incommunityteam(request,id):
    communnity=Communnity.objects.get(id = id)
    team=communnity.team.all();
    flag = False
    for member in team:
        if request.user == member.user_id:
            flag=True
            break
    return flag

def isteamleader(request,id):
    communnity=Communnity.objects.get(id = id)
    team=communnity.team.all();
    flag = False
    for member in team:
        if request.user == member.user_id and (member.role=='Team Leader' or member.role=="Vise"):
            flag=True
            break
    return flag