from django.db import models
from modules.level.models import Level
# Create your models here.


class File(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='Files')


class Video(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()


class Problem(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()


class Content(models.Model):
    name = models.CharField(max_length=50)
    level = models.ForeignKey(Level,
                              related_name='contents',
                              on_delete=models.CASCADE)
    files = models.ManyToManyField(
        File, related_name='files',blank=True)
    problems = models.ManyToManyField(
        Problem, related_name='problems',blank=True)
    videos = models.ManyToManyField(
        Video, related_name='videos',blank=True)

    description = models.TextField()

    def get_community(self):
        return self.level.get_community()

    def __str__(self):
        return str(self.level.name)
