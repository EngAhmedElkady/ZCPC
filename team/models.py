# team/models.py
from django.db import models
from communnity.models import Communnity
from django.contrib.auth import get_user_model

User = get_user_model()

# create team model
ROLCHOICE = (
    ('l' , 'leader'),
    ('s' , 'student'),
    ('t' ,  'team member')
)

class Team(models.Model):
    user_id = models.ForeignKey(User ,on_delete=models.CASCADE)
    community_id = models.ForeignKey(Communnity , on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rol = models.CharField(choices=ROLCHOICE , max_length=50)


    def __str__(self):
        return str(self.user_id.username)
