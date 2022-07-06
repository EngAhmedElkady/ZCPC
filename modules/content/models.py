from django.db import models
from requests import delete
from modules.level.models import Level
# Create your models here.


class Content(models.Model):
    name = models.CharField(max_length=50)
    level = models.ForeignKey(Level,
                              related_name='contents',
                              on_delete=models.CASCADE)

    description = models.TextField(blank=True,null=True)

    def get_community(self):
        return self.level.get_community()

    def __str__(self):
        return str(self.name)


class File(models.Model):
    content=models.ForeignKey(Content,related_name='files',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='Files')


class Video(models.Model):
    content=models.ForeignKey(Content,related_name='videos',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.URLField()


class Problem(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()


