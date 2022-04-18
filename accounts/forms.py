# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

<<<<<<< HEAD
from .models import CustomUser
=======
from django.contrib.auth import get_user_model
>>>>>>> origin/main


class CustomUserCreationForm(UserCreationForm):

    class Meta:
<<<<<<< HEAD
        model = CustomUser
        fields = ("username", "email", "codeforces_account")
=======
        model = get_user_model()
        fields = ("username", "email")
>>>>>>> origin/main


class CustomUserChangeForm(UserChangeForm):

    class Meta:
<<<<<<< HEAD
        model = CustomUser
=======
        model = get_user_model()
>>>>>>> origin/main
        fields = ("username", "email")
