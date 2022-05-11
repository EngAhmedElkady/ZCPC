from .models import Level, LevelFeedback, LevelTeam, Student, TeamFeedback
from .serializers import *
from modules.communnity.models import Communnity
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam, IsTeamLeader, IsOwner
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
# help function
from permissions.helpfunction import isteamleader, incommunityteam, isinlevelteam, isinlevelstudent


# Round
class viewsets_level(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = {
        IsInCommunnityTeam & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list', 'create'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def list(self, request,community_name,round_slug):
        communnity=None
        try:
            communnity=Communnity.objects.get(name=community_name)     
        except:
            return Response("community not found")
        try:
            rounds=communnity.rounds.all()
            round=rounds.get(slug=round_slug)
            levels=round.levels.all()
            serializer = LevelSerializer(levels,many=True)
            return Response(serializer.data)
        except:
            return Response("round not found")
            

    def create(self, request):
        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid():
            round_id = request.data['round']
            round = Round.objects.get(id=round_id)
            if incommunityteam(request.user.id, round.get_community()):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access, you should be in the team of this community"
                )


@api_view(['GET'])
def roundlevels(request):
    pass


class viewsets_levelteam(viewsets.ModelViewSet):
    queryset = LevelTeam.objects.all()
    serializer_class = LevelTeamSerializer
    permission_classes = {
        IsTeamLeader & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = LevelTeamSerializer(data=request.data)
        if serializer.is_valid():
            level_id = request.data['level']
            level = Level.objects.get(id=level_id)
            community_id = level.get_community()
            if isteamleader(request.user.id, community_id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )


class viewsets_student(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = {
        AllowAny & IsAuthenticated: ['post', 'retrieve', 'list', 'create'],
        (IsOwner & IsAuthenticated) | IsTeamLeader: ['retrieve', 'destroy', 'update', 'partial_update']
    }

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            level_id = request.data['level']
            level = Level.objects.get(id=level_id)
            if(level.status == False):
                return Response("The Round Closed")
            if(request.data['user'] != str(request.user.id)):
                print(type(request.data['user']), type(request.user.id))
                print('1' == 1)
                return Response("make sure you are user")

            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK,
            )


class viewsets_levelfeedback(viewsets.ModelViewSet):
    queryset = LevelFeedback.objects.all()
    serializer_class = LevelFeedbackSerializer
    permission_classes = {
        (IsTeamLeader & IsAuthenticated) | IsOwner: ['update', 'partial_update', 'destroy', 'list'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = LevelFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            level_id = request.data['level']
            if isinlevelstudent(request.data['user'], level_id) == False or str(request.user.id) != request.data['user']:
                return Response("sure you in this round")

            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK,
            )

        return Response(
            status.HTTP_400_BAD_REQUEST
        )


class viewsets_teamfeedback(viewsets.ModelViewSet):
    queryset = TeamFeedback.objects.all()
    serializer_class = TeamFeedbackSerializer
    permission_classes = {
        (IsTeamLeader & IsAuthenticated) | IsOwner: ['update', 'partial_update', 'destroy', 'list'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = TeamFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            level_id = request.data['level']
            if request.user.id != int(request.data['user']) or isinlevelstudent(request.user.id, level_id) == False or isinlevelteam(request.data['team_member'], level_id) == False:
                return Response("sure you in this round")

            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK,
            )

        return Response(
            status.HTTP_400_BAD_REQUEST
        )
