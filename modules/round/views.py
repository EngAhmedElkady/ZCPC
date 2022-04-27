from modules.communnity.models import Communnity
from .models import Round
from .serializers import RoundSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class DisplayAllRounds(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, communnity_id, *args, **kwargs):
        communnity = Communnity.objects.get(id=communnity_id)
        rounds = communnity.rounds.all()
        count = rounds.count()
        serializer = RoundSerializer(rounds, many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No Rounds"
            })


class DisplayUpdateDeleteRound(APIView):
    permission_classes=[IsInCommunnityTeam & IsAuthenticated]
    
    def get(self, request, round_id, *args, **kwargs):
        try:
            rounds = Round.objects.get(id=round_id)
            serializer = RoundSerializer(rounds)
            return Response(serializer.data)
        except:
            return Response({
                "message": "No Rounds"
            })
            
    def post(self, request):
        serializer = RoundSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status= status.HTTP_400_BAD_REQUEST
        )        
    
    def put(self, request,round_id,*args, **kwargs):
        round = Round.objects.get(id=round_id) 
        serializer = RoundSerializer(round, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request,round_id,*args, **kwargs):
        try:
            rounds = Round.objects.get(id=round_id)
            communnity=Communnity.objects.get(id=rounds.communnity_id)
            team=communnity.team.all();
            print(team)
            rounds.delete()
            return Response({
                "message": "deleted"
            })
        except:
            return Response({
                "message": "No Rounds"
            })
            
    
        
