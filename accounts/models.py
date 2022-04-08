# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,unique=False)
    bio = models.TextField(max_length=500, default="ahmed")
    codeforces_account=models.CharField(max_length=200)
    email = models.EmailField(max_length=500,unique=True)
    photo = models.ImageField(upload_to='media/images/')
    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
