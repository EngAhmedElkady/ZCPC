from modules.communnity.models import Communnity
from .models import Round
from .serializers import RoundApi
from rest_framework.views import APIView
from rest_framework.response import Response
from permissions.round import IsInCommunnityTeamOrNot
from rest_framework.decorators import permission_classes
# Create your views here.


class DisplayAllRounds(APIView):
    def get(self, request, communnity_id, *args, **kwargs):
        communnity = Communnity.objects.get(id=communnity_id)
        rounds = communnity.rounds.all()
        count = rounds.count()
        serializer = RoundApi(rounds, many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No Rounds"
            })


class DisplayUpdateDeleteRound(APIView):
    def get(self, request, round_id, *args, **kwargs):
        try:
            rounds = Round.objects.get(id=round_id)
            serializer = RoundApi(rounds)
            return Response(serializer.data)
        except:
            return Response({
                "message": "No Rounds"
            })
    @permission_classes([IsInCommunnityTeamOrNot])
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
        
