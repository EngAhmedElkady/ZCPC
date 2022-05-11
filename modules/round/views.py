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
    
    def retrieve(self, request, community_name,round_name, *args, **kwargs):
        communnity=None
        try:
            communnity=Communnity.objects.get(name=community_name)     
        except:
            return Response("community not found")
        print(communnity)
        try:
            rounds=communnity.rounds.all()
            round=rounds.get(name=round_name)
            serializer = RoundSerializer(round)
            return Response(serializer.data)
        except:
            return Response("round not found")
            
            
    
    def list(self, request,community_name):
        communnity=None
        try:
            communnity=Communnity.objects.get(name=community_name)       
            rounds=communnity.rounds.all()
            serializer = RoundSerializer(rounds , many=True)
            return Response(serializer.data)
        except:
            return Response("community not found")
        


    def create(self, request,community_name):
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



