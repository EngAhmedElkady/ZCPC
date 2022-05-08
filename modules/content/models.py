from re import L
from django.db import models
from modules.level.models import Level
# Create your models here.
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Content(models.Model):
    level = models.ForeignKey(Level,
                              related_name='contents',
                              on_delete=models.CASCADE)
    
    description = models.TextField()
    
    def get_community(self):
        return self.level.get_community()
    
    def __str__(self):
        return str(self.level.name)
   

class File(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='files')
    content=models.ForeignKey(Content, related_name='files',on_delete=models.CASCADE)
    

class Video(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    content=models.ForeignKey(Content, related_name='videos',on_delete=models.CASCADE)

class Problem(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    content=models.ForeignKey(Content, related_name='problems',on_delete=models.CASCADE)

