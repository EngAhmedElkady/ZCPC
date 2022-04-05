# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class CustomUser(AbstractUser):
    cv = models.FileField(upload_to='decomends', default="")
    bio = models.TextField(max_length=500, default="ahmed")
    phone = models.CharField(max_length=13, default="01140369670")

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
