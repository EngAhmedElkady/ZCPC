# communnity/models.py
from django.db import models
from django.contrib.auth import get_user_model
# get the user
 
User = get_user_model()

# create communnity model
# delete owner field from Community model --
class Communnity(models.Model):
    '''
        - all community has name, university, owner, createed_at
        - you cant create community if yout not loggedin  
    '''
    name = models.CharField(max_length=100)
    university= models.CharField(max_length=130)
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name  = "Community"
        verbose_name_plural = "Communities"


    def __str__(self):
        # display the name of the community
        return self.name
    
    
ROLE = (
        ('m' , 'member'),
        ('l' , 'leader')
    )
class Team(models.Model):
    '''
        - all Teams created has role and start journey, end journey and status
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    communnity_id=models.ForeignKey(Communnity,on_delete=models.CASCADE,related_name='team')
    role=models.CharField(max_length=100,choices=ROLE , default="member")
    start_journey=models.DateTimeField(auto_now_add=True)
    end_journey=models.DateTimeField(blank=True,null=True)
    status=models.BooleanField(default=True)
    
    class Meta:
        verbose_name  = "Team"
        verbose_name_plural = "Teams"


    def __str__(self):
        # display the userm community and role 
        return f"{self.user_id} work at {self.communnity_id} as {self.role}"
    