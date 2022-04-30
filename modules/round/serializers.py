from rest_framework import serializers
from .models import Round, RoundTeam, Student, TeamFeedback, RoundFeedback

# create round api


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'
        
        
class RoundTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundTeam
        fields=('id','user','round','role','id','get_community')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields='__all__'


class RoundFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundFeedback
        fields='__all__'


class TeamFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFeedback
        fields='__all__'
