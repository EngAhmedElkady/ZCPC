# post/models.py
from django.db import models
from communnity.models import Communnity
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()
# create post model
class Post(models.Model):
    auther = models.CharField(max_length=100)
    content = models.TextField(max_length=400)
    title = models.CharField(max_length=100)
    community = models.ForeignKey(Communnity , on_delete=models.CASCADE)
    #tag = models.IntegerField()
    def __str__(self):
        return self.title

