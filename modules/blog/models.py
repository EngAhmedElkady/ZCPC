# blog/models.py
from django.db import models
from modules.communnity.models import Communnity
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
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
    slug = models.SlugField(max_length=244 , null=True , blank=True)
    tags = TaggableManager()


    def __str__(self):
        return self.title # display the title of the post
    

    def get_community(self):
        communityId = self.community.id
        return communityId
    

    def save(self  , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Post , self).save(*args, **kwargs)


# create comment model
class Comment(models.Model):
    '''
        - The your can create comment if he is logged in
        - The comment contain user id, post id and the content
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)

    def __str__(self):
        return f' {self.post.title} , {self.user.username}' #  display the title of the post and the username of the user  
