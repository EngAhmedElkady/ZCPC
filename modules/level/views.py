from .models import Level, LevelFeedback, LevelTeam, Student, TeamFeedback
from .serializers import *
from modules.round.models import Round
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam, IsTeamLeader, IsOwner
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
# help function
from permissions.helpfunction import isteamleader, incommunityteam, isinlevelteam, isinlevelstudent


# Level

class GetLevelAndCreate(APIView):
    permission_classes = [IsAuthenticated]
    # get all level

    def get(self, request, round_id, *args, **kwargs):
        try:
            round = Round.objects.get(id=round_id)
            levels = round.levels.all()
            serializers = LevelSerializer(levels, many=True)
            return Response(serializers.data)
        except:
            return Response({
                "message": "round not found"
            }, status=status.HTTP_400_BAD_REQUEST)


    # create new level
    def post(self, request, round_id):
        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid():
            try:
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
            except :
                return Response({
                "message": "Round not found"
                }, status=status.HTTP_400_BAD_REQUEST)


class GetLevelAndUpdateAndDelete(APIView):
    permission_classes = [IsInCommunnityTeam, IsAuthenticated]
    # get community

    def get(self, request, pk,  *args, **kwagrs):
        try:
            levels = Level.objects.get(id=pk)
            serializer = LevelSerializer(levels)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            }, status=status.HTTP_400_BAD_REQUEST)
    # update community

    def put(self, request, pk, format=None):
        level = Level.objects.get(id=pk)
        serializer = LevelSerializer(level, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete community

    def delete(self, request, pk,  *args, **kwagrs):
        level = Level.objects.get(id=pk)
        level.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------
#  Level Team

class GetLevelTeamAndCreate(APIView):
    permission_classes = [IsAuthenticated]
    # get all level

    def get(self, request, level_id, *args, **kwargs):
        try:
            level = Level.objects.get(id=level_id)
            team = level.team.all()
            serializers = LevelTeamSerializer(team, many=True)
            return Response(serializers.data)
        except:
            return Response({
                "message": "level not found"
            }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, level_id):
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


class GetLevelTeamAndUpdateAndDelete(APIView):
    permission_classes = [IsInCommunnityTeam, IsAuthenticated]
    # get community

    def get(self, request, pk,  *args, **kwagrs):
        try:
            team = LevelTeam.objects.get(id=pk)
            serializer = LevelTeamSerializer(team)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            }, status=status.HTTP_400_BAD_REQUEST)
    # update community

    def put(self, request, pk, format=None):
        team = LevelTeam.objects.get(id=pk)
        serializer = LevelSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete community

    def delete(self, request, pk,  *args, **kwagrs):
        team = LevelTeam.objects.get(id=pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------
# student

class GetLevelStudentAndCreate(APIView):
    permission_classes = [IsAuthenticated]
    # get all level

    def get(self, request, level_id, *args, **kwargs):
        try:
            level = Level.objects.get(id=level_id)
            student = level.student.all()
            serializers = StudentSerializer(student, many=True)
            return Response(serializers.data)
        except :
            return Response({
                "message": "level not found"
            }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, level_id=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            level_id = request.data['level']
            level = Level.objects.get(id=level_id)
            if(level.status == False):
                return Response("The Round Closed")
            if(request.data['user'] != str(request.user.id)):
                return Response("make sure you are user")

            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK,
            )


class GetLevelstudentAndUpdateAndDelete(APIView):
    permission_classes = [IsAuthenticated and (IsInCommunnityTeam or IsOwner)]

    def get(self, request, pk,  *args, **kwagrs):
        try:
            student = Student.objects.get(id=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete community

    def delete(self, request, pk,  *args, **kwagrs):
        student = Student.objects.get(id=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------
#  level feedback
class GetLevelFeedbackAndCreate(APIView):
    permission_classes = [IsAuthenticated]
    # get all levelfeedback
    def get(self, request, level_id, *args, **kwargs):
        try:
            level = Level.objects.get(id=level_id)
            feedbacks = level.feedback.all()
            serializers = LevelFeedbackSerializer(feedbacks, many=True)
            return Response(serializers.data)
        except :
            return Response({
                "message": "level not found"
            }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request,level_id):
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


class GetLevelfeedbacktAndUpdateAndDelete(APIView):
    permission_classes = [IsAuthenticated and (IsOwner or IsTeamLeader)]

    def get(self, request, pk,  *args, **kwagrs):
        try:
            feedback = LevelFeedback.objects.get(id=pk)
            serializer = LevelFeedbackSerializer(feedback)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        feedback = LevelFeedback.objects.get(id=pk)
        serializer = LevelFeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete community

    def delete(self, request, pk,  *args, **kwagrs):
        feedback = LevelFeedback.objects.get(id=pk)
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# -------------------------------------------------------------


class GetTeamFeedbackAndCreate(APIView):
    permission_classes = [IsAuthenticated]
    # get all levelfeedback
    def get(self, request, level_id, *args, **kwargs):
        try:
            level = Level.objects.get(id=level_id)
            teamfeedback = level.teamfeedback.all()
            serializers = TeamFeedbackSerializer(teamfeedback, many=True)
            return Response(serializers.data)
        except :
            return Response({
                "message": "level not found"
            }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
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



class GetTeamfeedbacktAndUpdateAndDelete(APIView):
    permission_classes = [IsAuthenticated and (IsOwner or IsTeamLeader)]

    def get(self, request, pk,  *args, **kwagrs):
        try:
            teamfeedback = TeamFeedback.objects.get(id=pk)
            serializer = TeamFeedbackSerializer(teamfeedback)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        teamfeedback = TeamFeedback.objects.get(id=pk)
        serializer = TeamFeedbackSerializer(teamfeedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete community

    def delete(self, request, pk,  *args, **kwagrs):
        teamfeedback = TeamFeedback.objects.get(id=pk)
        teamfeedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# -------------------------------------------------------------