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
    start_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name  = "Community"
        verbose_name_plural = "Communities"


    def __str__(self):
        return self.name