from datetime import datetime
from typing_extensions import Required
from django import http
from rest_framework.response import Response
from rest_framework import serializers
from .models import Community, Team
from django.contrib.auth import get_user_model


# create communnity api
User = get_user_model()


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'slug': {'read_only': True},
            'owner': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['owner'] = self.context['owner']
        comminity = Community.objects.create(
            **validated_data)  # saving post object
        return comminity

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.university = validated_data.get(
            'university', instance.university)
        instance.image = validated_data.get('image', instance.image)
        instance.bio = validated_data.get('bio', instance.bio)

        instance.save()
        return instance


class AddTMemeberTeam(serializers.Serializer):
    email = serializers.EmailField(required=True)
    role = serializers.CharField(max_length=200)
    status = serializers.BooleanField()

    def validate_memeber(self, email):
        try:
            member = User.objects.get(email=email)
        except:
            raise http.Http404("user not found")

        community = self.context['community']

        teams = community.team.all()
        for item in teams:
            if item.user == member:
                raise http.Http404("user already in team")
        return member

    def create(self, validated_data):
        community = self.context['community']
        member = self.validate_memeber(validated_data.get('email'))
        team = Team.objects.create(user=member, community=community, role=validated_data.get(
            'role', 'member'), status=validated_data.get('status', False))  # saving team object
        return team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['user', "username", 'community', 'role',
                  'start_journey', 'end_journey', 'status']
        extra_kwargs = {
            'user': {'read_only': True},
            'community': {'read_only': True},
            'end_journey': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.status = validated_data.get(
            'status', instance.status)

        if instance.status == False:
            instance.end_journey = datetime.now()
        else:
            instance.end_journey = None

        instance.save()
        return instance
