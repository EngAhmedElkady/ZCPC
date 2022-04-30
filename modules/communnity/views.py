from .models import Communnity, Team
from .serializers import ComnunityApi,TeamApi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from permissions.team import isOwner
# create apis for community 
# display all coummunity
class DisplayAllCommunity(APIView):
    def get(self , request , *args , **kwargs):
        communites = Communnity.objects.all()
        count = Communnity.objects.all().count()
        serializer = ComnunityApi(communites , many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No community"
            })


class CreateNewCommunity(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self , request , *args , **kwargs):
        return Response({
            "message": "create new community"
        })
    def post(self , request , *args , **kwargs):
        serializer = ComnunityApi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)




class UpdateCommunity(APIView):
    permission_classes = [isOwner]
    def put(self, request, pk, format=None):
        community = Communnity.objects.get(id=pk)
        serializer = ComnunityApi(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommunity(APIView):
    permission_classes = [isOwner]
    def delete(self , request , community_id ,  *args , **kwagrs):
        community = Communnity.objects.get(id=community_id)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DisplayCommunityTeam(APIView):
    def get(self , request , community_id,*args , **kwargs):
        community = Communnity.objects.get(id=community_id)
        team=community.team.all()
        serializer = TeamApi(team , many=True)
        return Response(serializer.data)
        


# create apis for team

class DisplayAllTeams(APIView):
    def get(self , request , *args , **kwargs):
        teams = Team.objects.all()
        serializer  = TeamApi(teams , many=True)
        return Response(serializer.data)


class CreateTeam(APIView):
    permission_classes = [isOwner]
    def post(self , request , *args , **kwargs):
        serializer = TeamApi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class DisplaySingleTeam(APIView):
    def get(self , request ,team_id ,  *args , **kwargs):
        team = Team.objects.get(id=team_id)
        serializer = TeamApi(team)
        return Response(serializer.data)


class DeleteTeam(APIView):
    permission_classes = [isOwner]
    def delete(self , request , team_id ,  *args , **kwagrs):
        team = Team.objects.get(id=team_id)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UpdateTeam(APIView):
    permission_classes = [isOwner]
    def put(self, request, pk, format=None):
        team = Team.objects.get(id=pk)
        serializer = TeamApi(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)