# accounts/views.py
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model
User = get_user_model()



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve Current User
class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    model = User
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class UpdateUserAPIView(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)        
        if serializer.is_valid():
            self.object.name=request.data.get('name',self.object.name)
            self.object.bio=request.data.get('bio',self.object.bio)
            self.object.codeforces_account=request.data.get('codeforces_account',self.object.codeforces_account)
            self.object.github_account=request.data.get('github_account',self.object.github_account)
            self.object.save()
            return Response(UserSerializer(self.object, context=self.get_serializer_context()).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    