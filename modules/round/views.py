from urllib import response
from modules.communnity.models import Communnity
from .models import Round, RoundTeam
from .serializers import RoundSerializer, RoundTeamSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

# help function 

def incommunityteam(request,id):
    communnity=Communnity.objects.get(id = id)
    team=communnity.team.all();
    flag = False
    for member in team:
        if request.user == member.user_id and (member.role=='Team Leader' or member.role=="Vise"):
            flag=True
            break
    return flag

# Round
class viewsets_round(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = {
        IsInCommunnityTeam & IsAuthenticated: ['update','post', 'partial_update', 'destroy', 'list', 'create'],
        AllowAny& IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = RoundSerializer(data=request.data)
        if serializer.is_valid():
            id = request.data['communnity']
            if incommunityteam(request,id):
                serializer.save()
                return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
                )
            else:
                return Response(
                   "you don't have access"
                )

# Round Team
class viewsets_roundteam(viewsets.ModelViewSet):
    queryset=RoundTeam.objects.all()
    serializer_class=RoundTeamSerializer
    permission_classes = {
        IsInCommunnityTeam & IsAuthenticated: ['update','post', 'partial_update', 'destroy', 'list'],
        AllowAny& IsAuthenticated: ['retrieve']
    }
    def create(self, request):
        serializer = RoundTeamSerializer(data=request.data)
        if serializer.is_valid():
            round_id = request.data['round']
            round=Round.objects.get(id=round_id);
            community_id=round.communnity.id
            if incommunityteam(request,community_id):
                serializer.save()
                return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
                )
            else:
                return Response(
                   "you don't have access"
                )
