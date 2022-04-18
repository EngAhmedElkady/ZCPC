# blog/models.py
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




# create comment model
class Comment(models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post , on_delete=models.CASCADE)
    content = models.TextField(max_length=200)

    def __str__(self):
        return f' {self.post_id.title} , {self.user_id.username} '