from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators

User = get_user_model()

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data 
    """
    class Meta:
        model = User
        exclude = ("id",)


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'codeforces',
                  'telegram', 'email', 'password')
        # not return in serializer data
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(username=validated_data['username'],
                                        codeforces=validated_data['codeforces'],
                                        telegram=validated_data['telegram'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UpdateUserSerializer(serializers.Serializer):
    model = User
    """
    Serializer for update user endpoint.
    """
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    codeforces = serializers.CharField(required=False)
    telegram = serializers.URLField(required=False)
    github = serializers.URLField(required=False)
    linkedin = serializers.URLField(required=False)
    university = serializers.CharField(required=False)
