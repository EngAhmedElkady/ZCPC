from rest_framework import serializers
from .models import Level, LevelTeam, Student, TeamFeedback, LevelFeedback

# create round api


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
        extra_kwargs = {
            'round': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['round']=self.context['round']
        level = Level.objects.create(
            **validated_data)
        return level

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


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
