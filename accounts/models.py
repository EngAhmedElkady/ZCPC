# accounts/models.py
from distutils.command.upload import upload
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.username, filename)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    upload = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    codeforces_account = models.CharField(max_length=100)
    github_account = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:

        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
