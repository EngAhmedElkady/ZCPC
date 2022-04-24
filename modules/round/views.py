from .models import Round
from .serializers import RoundApi
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class DisplayAllRounds(APIView):
    def get(self, request, communnity_id, *args, **kwargs):
        rounds = Round.objects.filter(commmunity_id=communnity_id)
        count = rounds.count()
        serializer = RoundApi(rounds, many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No community"
            })


class DisplayUpdateDeleteRound(APIView):
    def get(self, request, communnity_id, round_id, *args, **kwargs):
        try:
            rounds = Round.objects.get(
                commmunity_id=communnity_id, round_id=round_id)
            serializer = RoundApi(rounds, many=True)
            return Response(serializer.data)
        except:
            return Response({
                "message": "No Rounds"
            })
