from ast import Is
import re
from django.http import Http404
from .models import Level, LevelTeam, Student, LevelFeedback

from .serializers import *
from modules.community.models import Community
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from permissions.community import *
from django.contrib.auth import get_user_model
from permissions.helpfunction import Community_Function
from django.shortcuts import get_object_or_404


User = get_user_model()
# level


class viewsets_level(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    lookup_field = 'name'

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'create']:
            self.permission_classes = [IsAuthenticated, IsInCommunnityTeam]
        elif self.action == 'destroy':
            self.permission_classes = [IsTeamLeader_OR_VICE]

        return [permission() for permission in self.permission_classes]

    def get_community(self, community_slug):
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community not found")

    def get_object(self, community_slug, round_slug, name):
        community_ = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(
            queryset, community=community_, slug=round_slug)
        levels = round.levels.all()
        level = get_object_or_404(levels, name=name)
        self.check_object_permissions(self.request, community_)
        return level

    def list(self, request, community_slug, round_slug):
        community = self.get_community(community_slug)
        rounds = community.rounds.all()
        round = get_object_or_404(
            rounds, community=community, slug=round_slug)
        levels = round.levels.all()
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, community_slug, round_slug, name, *args, **kwargs):
        instance = self.get_object(community_slug, round_slug, name)
        serializer = LevelSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, community_slug, round_slug, name, *args, **kwargs):
        instance = self.get_object(community_slug, round_slug, name)
        data = {
            "name": request.data.get('name', instance.name),
            "description": request.data.get('description', None),
            "status": request.data.get('status', instance.status)
        }
        serializer = LevelSerializer(instance=instance,
                                     data=data,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_slug, round_slug, name, *args, **kwargs):
        instance = self.get_object(community_slug, round_slug, name)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, community_slug, round_slug):

        community = self.get_community(community_slug)
        rounds = community.rounds.all()
        round = get_object_or_404(
            rounds, community=community, slug=round_slug)
        self.check_object_permissions(self.request, community)
        serializer = LevelSerializer(
            data=request.data, context={'round': round})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class viewsets_levelteam(viewsets.ModelViewSet):
    queryset = LevelTeam.objects.all()
    serializer_class = LevelTeamSerializer
    lookup_field = 'user__username'

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'create']:
            self.permission_classes = [IsAuthenticated, IsInCommunnityTeam]
        elif self.action in ['destroy']:
            self.permission_classes = [IsTeamLeader_OR_VICE]

        return [permission() for permission in self.permission_classes]

    def get_community(self, community_slug):
        community = None
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community not found")

    def get_object(self, community_slug, round_slug, name):
        community = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(
            queryset, community=community, slug=round_slug)
        levels = round.levels.all()
        level = get_object_or_404(levels, name=name)
        self.check_object_permissions(self.request, community)
        return level

    def create(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        try:
            user = User.objects.get(id=request.data.get('user'))
        except:
            raise Http404("User not found")

        if not Community_Function.is_in_community_team(user, level):
            return Response("User is not in the community team", status=status.HTTP_403_FORBIDDEN)

        serializer = LevelTeamSerializer(
            data=request.data, context={'level': level})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        serializers = LevelTeamSerializer(level.team.all(), many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        level_team = get_object_or_404(
            level.team.all(), user__username=user__username)
        serializers = LevelTeamSerializer(level_team)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        team_member = get_object_or_404(
            level.team.all(), user__username=user__username)
        data = {
            "role": request.data.get('role', team_member.role),
        }
        serializer = LevelTeamSerializer(instance=team_member,
                                         data=data,
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        team_member = get_object_or_404(
            level.team.all(), user__username=user__username)
        data = {
            "role": request.data.get('role', team_member.role),
        }
        serializer = LevelTeamSerializer(instance=team_member,
                                         data=data,
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        team_member = get_object_or_404(
            level.team.all(), user__username=user__username)
        team_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class viewsets_level_student(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'user__username'

    def get_permissions(self):

        if self.action in ['list', 'retrieve', 'create','destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsInCommunnityTeam]
    
        return [permission() for permission in self.permission_classes]

    def get_community(self, community_slug):
        community = None
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community not found")

    def get_object(self, community_slug, round_slug, name):
        community = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(
            queryset, community=community, slug=round_slug)
        levels = round.levels.all()
        level = get_object_or_404(levels, name=name)
        self.check_object_permissions(self.request, community)
        return level

    def list(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        students = level.students.all()
        serializers = StudentSerializer(students, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        student = get_object_or_404(
            level.students.all(), user__username=user__username)
        serializers = StudentSerializer(student)
        return Response(data=serializers.data, status=status.HTTP_200_OK)


    def update(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        student = get_object_or_404(
            level.students.all(), user__username=user__username)
        data = {
            "status": request.data.get('status', student.status),
        }
        serializer = StudentSerializer(instance=student,
                                       data=data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        student = get_object_or_404(
            level.students.all(), user__username=user__username)
        data = {
            "status": request.data.get('status', student.status),
        }
        serializer = StudentSerializer(instance=student,
                                       data=data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        data = {
            'user': request.user.id,
            'status': request.data.get('status', True),
        }

        serializer = StudentSerializer(data=data, context={'level': level})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        student = get_object_or_404(
            level.students.all(), user__username=user__username)
        if not Community_Function.is_owner(request.user,student.user) and not Community_Function.is_in_community_team(request.user,student):
           return Response(status=status.HTTP_403_FORBIDDEN)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class viewsets_levelfeedback(viewsets.ModelViewSet):
    
    queryset=LevelFeedback.objects.all()
    serializer_class=LevelFeedbackSerializer
    lookup_field='id'
    
    def get_community(self, community_slug):
        community = None
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community not found")
        
    def get_object(self, community_slug, round_slug, name):
        community = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(
            queryset, community=community, slug=round_slug)
        levels = round.levels.all()
        level = get_object_or_404(levels, name=name)
        return level
    
    def list(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        feedbacks = level.feedbacks.all()
        serializers = LevelFeedbackSerializer(feedbacks, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
   
    def retrieve(self, request, community_slug, round_slug, name, id, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        feedback = get_object_or_404(
            level.feedbacks.all(), id=id)
        serializers = LevelFeedbackSerializer(feedback)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
        
    def update(self, request, community_slug, round_slug, name, id,*args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        feedback = get_object_or_404(
            level.feedbacks.all(), id=id)
        data = {
            "feedback": request.data.get('feedback', feedback.feedback),
            "stars":request.data.get('stars', feedback.stars),
        }
        
        if not Community_Function.is_owner(request.user,feedback.student):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        serializer = LevelFeedbackSerializer(instance=feedback,
                                             data=data,
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, community_slug, round_slug, name, id, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        feedback = get_object_or_404(
            level.feedbacks.all(), id=id)
        data = {
            "feedback": request.data.get('feedback', feedback.feedback),
            "stars":request.data.get('stars', feedback.stars),
        }
        
        if not Community_Function.is_owner(request.user,feedback.student):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        serializer = LevelFeedbackSerializer(instance=feedback,
                                             data=data,
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def create(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        if not Community_Function.is_in_level_student(request.user,level):
            return Response(status=status.HTTP_403_FORBIDDEN,data={'detail':'You are not in this level'})
        student=Student.objects.get(level=level,user=request.user)
        data = {
            'student': student.id,
            'level': level.id,
            'stars': request.data.get('stars'),
            'feedback': request.data.get('feedback'),
        }
        serializer = LevelFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def destory(self, request, community_slug, round_slug, name, id, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        feedback = get_object_or_404(
            level.feedbacks.all(), id=id)
        if not Community_Function.is_teamleader_or_vise(request.user,level) :
               return Response(status=status.HTTP_403_FORBIDDEN)
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class viewsets_teamfeedback(viewsets.ModelViewSet):
    queryset=LevelTeamFeedback.objects.all()
    serializer_class=LevelTeamFeedbackSerializer
    lookup_field='id'
    
    def get_community(self, community_slug):
        community = None
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community not found")
        
    def get_level(self, community_slug, round_slug, name):
        community = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(
            queryset, community=community, slug=round_slug)
        levels = round.levels.all()
        level = get_object_or_404(levels, name=name)
        
        return level
    
    def list(self, request, community_slug, round_slug, name,username, *args, **kwargs):
        level = self.get_level(community_slug, round_slug, name)
        team=level.team.all()
        member=get_object_or_404(team,username=username)
        feedbacks = member.member_feedbacks.all()
        serializers = LevelTeamFeedbackSerializer(feedbacks, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
   
    def retrieve(self, request, community_slug, round_slug, name,username,id, *args, **kwargs):
        level = self.get_level(community_slug, round_slug, name)
        team=level.team.all()
        member=get_object_or_404(team,username=username)
        feedbacks = member.member_feedbacks.all()
        feedback=get_object_or_404(feedbacks,id=id)
        serializers = LevelTeamFeedbackSerializer(feedback)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
        
    def update(self, request, community_slug, round_slug, name, username,id,*args, **kwargs):
        level = self.get_level(community_slug, round_slug, name)
        team=level.team.all()
        member=get_object_or_404(team,username=username)
        feedbacks = member.member_feedbacks.all()
        feedback=get_object_or_404(feedbacks,id=id)
        data = {
            "feedback": request.data.get('feedback', feedback.feedback),
            "stars":request.data.get('stars', feedback.stars),
        }
        
        if not Community_Function.is_owner(request.user,feedback.student):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        serializer = LevelTeamFeedbackSerializer(instance=feedback,
                                             data=data,
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, community_slug, round_slug, name,username ,id, *args, **kwargs):
        level = self.get_level(community_slug, round_slug, name)
        team=level.team.all()
        member=get_object_or_404(team,username=username)
        feedbacks = member.member_feedbacks.all()
        feedback=get_object_or_404(feedbacks,id=id)
        data = {
            "feedback": request.data.get('feedback', feedback.feedback),
            "stars":request.data.get('stars', feedback.stars),
        }
        
        if not Community_Function.is_owner(request.user,feedback.student):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        serializer = LevelTeamFeedbackSerializer(instance=feedback,
                                             data=data,
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
            
    def create(self, request, community_slug, round_slug, name,username,*args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        if not Community_Function.is_in_level_student(request.user,level):
            return Response(status=status.HTTP_403_FORBIDDEN,data={'detail':'You are not in this level'})
        student=Student.objects.get(level=level,user=request.user)
        member=get_object_or_404(level.team.all(),username=username)
        data = {
            'student': student.id,
            'level': level.id,
            'team_member':member.id,
            'stars': request.data.get('stars'),
            'feedback': request.data.get('feedback'),
        }
        serializer = LevelTeamFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def destory(self, request, community_slug, round_slug, name,username,id, *args, **kwargs):
        level = self.get_level(community_slug, round_slug, name)
        team=level.team.all()
        member=get_object_or_404(team,username=username)
        feedbacks = member.member_feedbacks.all()
        feedback=get_object_or_404(feedbacks,id=id)
        if not Community_Function.is_teamleader_or_vise(request.user,level) :
               return Response(status=status.HTTP_403_FORBIDDEN)
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
  