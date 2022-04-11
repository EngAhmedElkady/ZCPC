from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators

User = get_user_model()

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username", "name", "email","bio","github_account","codeforces_account"]
        
        

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', "codeforces_account", 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                        codeforces_account=validated_data['codeforces_account'], password=validated_data['password'])
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
    bio = serializers.CharField(required=False)
    codeforces_account = serializers.CharField(required=False)
    github_account = serializers.CharField(required=False)
