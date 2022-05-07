from rest_framework import serializers
from .models import Level, LevelTeam, Student, TeamFeedback, LevelFeedback

# create round api


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class LevelTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTeam
        fields = ('id', 'user', 'level', 'role', 'id', 'get_community')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class LevelFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelFeedback
        fields = '__all__'


class TeamFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFeedback
        fields = '__all__'
