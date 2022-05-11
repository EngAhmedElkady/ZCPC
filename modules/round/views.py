from modules.communnity.models import Communnity
from .models import Round
from .serializers import RoundSerializer
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from permissions.helpfunction import  incommunityteam
from rest_framework.views import APIView


# help function


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
            if incommunityteam(request.user.id, id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )


class CommunityRounds(APIView):
    def get(self , request ,community_id ,*args , **kwargs):
        communnity=Communnity.objects.get(id=community_id)
        rounds=communnity.rounds.all()
        serializer = RoundSerializer(rounds , many=True)
        return Response(serializer.data)
    def post(self):
        pass

