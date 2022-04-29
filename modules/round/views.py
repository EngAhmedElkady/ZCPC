from urllib import response
from .models import Round, RoundTeam
from .serializers import RoundSerializer, RoundTeamSerializer
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam, IsTeamLeader
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
# help function
from .helpfunction import isteamleader, incommunityteam


# Round
class viewsets_round(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = {
        IsInCommunnityTeam & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list', 'create'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = RoundSerializer(data=request.data)
        if serializer.is_valid():
            id = request.data['communnity']
            if incommunityteam(request, id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )

# Round Team


class viewsets_roundteam(viewsets.ModelViewSet):
    queryset = RoundTeam.objects.all()
    serializer_class = RoundTeamSerializer
    permission_classes = {
        IsTeamLeader & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = RoundTeamSerializer(data=request.data)
        if serializer.is_valid():
            round_id = request.data['round']
            round = Round.objects.get(id=round_id)
            community_id = round.communnity.id
            if isteamleader(request, community_id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )
