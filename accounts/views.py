# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework import status, filters
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication


User = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# api
# -----------------------------------------------------------------------
# signup
class SignupViewSets(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            "user": serializer.data,
            'token': token.key,
        },
            status=status.HTTP_201_CREATED)


# login
class LoginViewSets(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            print(request.data["email"])
            print(request.data["password"])
            user = User.objects.get(
                email=request.data["email"], password=request.data["password"])
            print(user)
            token = Token.objects.get(user=user)

            return Response({
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                    "codeforces_account":user.codeforces_account,
                },
                'token': token.key,
            },
                status=status.HTTP_201_CREATED)

        except:
            return Response({
                "Bad request"
            },
                status=status.HTTP_400_BAD_REQUEST)
