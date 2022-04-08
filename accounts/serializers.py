from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "codeforces_account", "password")
        
        
    def validate_password(self, data):
            validators.validate_password(password=data, user=User)
            return data
        
        

    