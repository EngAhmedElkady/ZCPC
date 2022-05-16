from .models import Communnity, Team
from .serializers import ComnunityApi, TeamApi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework import permissions
from permissions.community import IsOwner
# create apis for community
# refactor community code 
class GetCommuntiesAndCreate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # get all communties
    def get(self , request , *args , **kwargs):
        communites = Communnity.objects.all()
        count = Communnity.objects.all().count()
        serializer = ComnunityApi(communites, many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No community"
            })
    # create new community
    def post(self , request , *args , **kwargs):
        serializer = ComnunityApi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class GetCommunityAndUpdateAndDelete(APIView):
    permission_classes = [IsOwner]
    # get community 
    def get(self , request ,slug ,  *args , **kwagrs):
        try:
            community = Communnity.objects.get(slug=slug)
            serializer = ComnunityApi(community)
            return Response(serializer.data)
        except:
            return Response({
                "message":"Error"
            } , status=status.HTTP_400_BAD_REQUEST)
    # update community
    def put(self, request, slug, format=None):
        community = Communnity.objects.get(slug=slug)
        serializer = ComnunityApi(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete community
    def delete(self , request , slug ,  *args , **kwagrs):
        community = Communnity.objects.get(slug=slug)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# display teams in community
class DisplayCommunityTeam(APIView):
    def get(self, request, slug, *args, **kwargs):
        community = Communnity.objects.get(slug=slug)
        team = community.team.all()
        serializer = TeamApi(team, many=True)
        return Response(serializer.data)

# check later
# class DisplayCommunity(APIView):
#     def get(self, request, slug, *args, **kwargs):
#         community = Communnity.objects.get(slug=slug)
#         serializer = ComnunityApi(community)
#         return Response(serializer.data)
        


# create apis for team
# refactor team code 

class GetTeamsAndCreate(APIView):
    # get all teams
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self , request , *args , **kwargs):
        teams = Team.objects.all()
        serializer  = TeamApi(teams , many=True)
        if teams.count() < 0 :
            return Response({
                "message": "No teams"
            })
        else:
            return Response(serializer.data)
    # crete new team
    def post(self , request , *args , **kwargs):
        serializer = TeamApi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class GetTeamAndUpdateAndDelete(APIView):
    permission_classes = [IsOwner]
    # get team
    def get(self , request ,pk ,  *args , **kwargs):
        team = Team.objects.get(id=pk)
        serializer = TeamApi(team)
        return Response(serializer.data)
    # update team
    def put(self, request, pk, format=None):
        team = Team.objects.get(id=pk)
        serializer = TeamApi(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete team
    def delete(self , request , pk ,  *args , **kwagrs):
        team = Team.objects.get(id=pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
