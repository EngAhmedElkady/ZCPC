from modules.communnity.models import Communnity
from .models import Round
from .serializers import RoundSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from permissions.helpfunction import incommunityteam
from rest_framework.views import APIView


# help function

# Round
class viewsets_round(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    lookup_field = 'round_name'

    def get_community(self, community_name):
        community = None
        try:
            community = Communnity.objects.get(slug=community_name)
            return community
        except:
            return Response("community not found")

    def retrieve(self, request, community_name, round_name, *args, **kwargs):
        try:
            community = self.get_community(community_name)
            rounds = community.rounds.all()
            round = rounds.get(slug=round_name)
            serializer = RoundSerializer(round)
            return Response(serializer.data)
        except:
            return Response("round not found")

    def update(self, request, community_name, round_name, *args, **kwargs):
        try:
            community = self.get_community(community_name)
            rounds = community.rounds.all()
            round = rounds.get(slug=round_name)
            serializer = RoundSerializer(round, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("round not found")

    def destroy(self, request, community_name, round_name, *args, **kwargs):
        # try:
        community = self.get_community(community_name)
        rounds = community.rounds.all()
        print(rounds)
        round = rounds.get(slug=round_name)
        round.delete()
        return Response("Done", status=status.HTTP_400_BAD_REQUEST)
        # except:
        return Response("round not found")

    def list(self, request, community_name):

        try:
            community = self.get_community(community_name)
            all_rounds = community.rounds.all()
            print(all_rounds)
            serializer = RoundSerializer(all_rounds, many=True)
            return Response(serializer.data)
        except:
            return Response("community not found")

    def create(self, request, community_name):
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
