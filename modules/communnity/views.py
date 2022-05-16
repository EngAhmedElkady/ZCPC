from .models import Communnity, Team
from .serializers import ComnunityApi, TeamApi
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from modules.communnity.models import Communnity
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from permissions.helpfunction import incommunityteam, isowner, isteamleader
# help function
User = get_user_model()


# Round
class viewsets_community(viewsets.ModelViewSet):
    queryset = Communnity.objects.all()
    serializer_class = ComnunityApi
    lookup_field = "slug"
    permission_classes = {
        IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list', 'create'],
        IsAuthenticated: ['retrieve']
    }

    def retrieve(self, request,slug, *args, **kwargs):
        try:
            communnity = Communnity.objects.get(slug=slug)
            serializer = ComnunityApi(communnity)
            return Response(serializer.data)
        except:
            return Response("Community not found")

    def list(self, request):
        try:
            communnities = Communnity.objects.all()
            serializer = ComnunityApi(communnities, many=True)
            return Response(serializer.data)
        except:
            return Response("community not found")

    def create(self, request):
        serializer = ComnunityApi(data=request.data)
        if serializer.is_valid():
            id = request.data['owner']
            if isowner(request.user.id, id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )


class viewsets_team(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamApi
    lookup_field ="slug"

    permission_classes = {
        IsInCommunnityTeam & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list', 'create'],
        IsAuthenticated: ['retrieve']
    }

    def retrieve(self, request, slug, username, *args, **kwargs):
        print(args, kwargs)
        try:
            communnity = Communnity.objects.get(slug=slug)
        except:
            return Response("community not found")

        try:
            user = User.objects.get(username=username)
            team = communnity.team.get(user=user)
            serializer = TeamApi(team)
            return Response(serializer.data)
        except:
            return Response("member not found")

    def list(self, request,*args, **kwargs):
        # slug=kwargs['slug']
        print("----------------------------------------------------")
        print(args, kwargs)

        try:
            communnity = Communnity.objects.get(slug=slug)
            team = communnity.team.all()
            serializer = TeamApi(team, many=True)
            return Response(serializer.data)
        except:
            return Response("community not found")

    def create(self, request):
        serializer = TeamApi(data=request.data)
        community_id = request.data['community']
        if serializer.is_valid():
            if incommunityteam(request.user.id, community_id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )
