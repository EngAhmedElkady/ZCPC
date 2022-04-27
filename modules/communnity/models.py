# communnity/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# create communnity model
# delete owner field from Community model --
class Communnity(models.Model):
    name = models.CharField(max_length=100)
    university= models.CharField(max_length=130)
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name  = "Community"
        verbose_name_plural = "Communities"


    def __str__(self):
        return self.name
    
    
class Team(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    communnity_id=models.ForeignKey(Communnity,on_delete=models.CASCADE,related_name='team')
    role=models.CharField(max_length=100,default="member")
    start_journey=models.DateTimeField(auto_now_add=True)
    end_journey=models.DateTimeField(blank=True,null=True)
    status=models.BooleanField(default=True)
    
    class Meta:
        verbose_name  = "Team"
        verbose_name_plural = "Teams"


    def __str__(self):
        return f"{self.user_id} work at {self.communnity_id} as {self.role}"
    