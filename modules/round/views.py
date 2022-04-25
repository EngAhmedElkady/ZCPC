from modules.communnity.models import Communnity
from .models import Round
from .serializers import RoundApi
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class DisplayAllRounds(APIView):
    def get(self, request, communnity_id, *args, **kwargs):
        communnity=Communnity.objects.get(id=communnity_id)
        rounds =communnity.rounds.all()
        count = rounds.count()
        serializer = RoundApi(rounds, many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No community"
            })


class DisplayUpdateDeleteRound(APIView):
    def get(self, request,round_id, *args, **kwargs):
        try:
            rounds = Round.objects.get(id=round_id)
            serializer = RoundApi(rounds)
            return Response(serializer.data)
        except:
            return Response({
                "message": "No Rounds"
            })


    