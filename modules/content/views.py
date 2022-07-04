from gc import get_objects
from urllib import response
from django.shortcuts import get_object_or_404, render
from . import serializers
from . import models
from modules.level.models import Level
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
# help function
from permissions.helpfunction import Community_Function
from permissions.community import *
from django.http import Http404
from django.contrib.auth import get_user_model

User = get_user_model()


class viewsets_content(viewsets.ModelViewSet):

    queryset = models.Content.objects.all()
    serializer_class = serializers.ContentSerializer
    lookup_field = 'id'

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
        pass

    def list(self, request, community_slug, round_slug, name, *args, **kwargs):
        level = self.get_object(community_slug, round_slug, name)
        contents = level.contents.all()
        print(level, contents)
        serializer = self.serializer_class(contents, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, community_slug, round_slug, name, id, *args, **kwargs):
        pass

    def update(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        pass

    def partial_update(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        pass

    def destroy(self, request, community_slug, round_slug, name, user__username, *args, **kwargs):
        pass
