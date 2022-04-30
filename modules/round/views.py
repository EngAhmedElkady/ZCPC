from urllib import response
from .models import Round, RoundFeedback, RoundTeam, Student, TeamFeedback
from .serializers import RoundSerializer, RoundTeamSerializer, StudentSerializer, RoundTeamSerializer, RoundFeedbackSerializer, TeamFeedbackSerializer
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam, IsTeamLeader, IsOwner
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
# help function
from .helpfunction import isteamleader, incommunityteam, isinroundteam


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
            if incommunityteam(request.user, id):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )

# Round Team


class viewsets_roundteam(viewsets.ModelViewSet):
    queryset = RoundTeam.objects.all()
    serializer_class = RoundTeamSerializer
    permission_classes = {
        IsTeamLeader & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = RoundTeamSerializer(data=request.data)
        if serializer.is_valid():
            round_id = request.data['round']
            round = Round.objects.get(id=round_id)
            community_id = round.communnity.id
            if isteamleader(request.user, community_id):
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
            round_id = request.data['round']
            round = Round.objects.get(id=round_id)
            if(round.status == False):
                return Response("The Round Closed")
            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK,
            )


class viewsets_roundfeedback(viewsets.ModelViewSet):
    queryset = RoundFeedback.objects.all()
    serializer_class = RoundFeedbackSerializer
    permission_classes = {
        (IsTeamLeader & IsAuthenticated) | IsOwner: ['update', 'partial_update', 'destroy', 'list'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def create(self, request):
        serializer = RoundFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            round_id = request.data['round']
            round = Round.objects.get(id=round_id)
            students = round.roundstudent.all()
            flag = False
            for student in students:
                if request.user == student.user:
                    flag = True
                    break

            if flag == False:
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
            round_id = request.data['round']
            round = Round.objects.get(id=round_id)
            students = round.roundstudent.all()
            flag = False
            for student in students:
                if request.user == student.user:
                    flag = True
                    break
            
            print("------------------->",request.data['team_member'])
            print("------------------->",flag)
            print("------------------->",isinroundteam(request.data['team_member'],round_id))
            if flag == False or isinroundteam(request.data['team_member'],round.id)==False:
                return Response("sure you in this round")

            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK,
            )

        return Response(
            status.HTTP_400_BAD_REQUEST
        )
