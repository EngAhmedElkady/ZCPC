# blog/models.py
from django.db import models
from modules.communnity.models import Communnity
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

# Create your models here.


User = get_user_model() # get the user
# create post model


class Post(models.Model):
    '''
        - The user can create post if he is logged in
        - the post contain auther, title, community, content, tag 
    '''
    auther = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=100)
    community = models.ForeignKey(Communnity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = TaggableManager()

    def __str__(self):
        return self.title # display the title of the post


# create comment model
class Comment(models.Model):
    '''
        - The your can create comment if he is logged in
        - The comment contain user id, post id and the content
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)

    def __str__(self):
        return f' {self.post_id.title} , {self.user_id.username}' #  display the title of the post and the username of the user  
