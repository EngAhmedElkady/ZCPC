from rest_framework import serializers
from .models import Level, LevelTeam, Student, LevelFeedback,LevelTeamFeedback

# create round api


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
        extra_kwargs = {
            'round': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['round'] = self.context['round']
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
        fields = ['user', "username", 'role', 'level']
        extra_kwargs = {
            'level': {'read_only': True},
            'username': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['level'] = self.context['level']
        level = LevelTeam.objects.create(
            **validated_data)
        return level

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'level': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['level'] = self.context['level']
        level = Student.objects.create(
            **validated_data)
        return level

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class LevelFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelFeedback
        fields = '__all__'

    def create(self, validated_data):
        levelfeedback = LevelFeedback.objects.create(
            **validated_data)
        return levelfeedback

    def update(self, instance, validated_data):
        instance.stars = validated_data.get('stars', instance.stars)
        instance.feedback = validated_data.get('feedback', instance.feedback)
        instance.save()
        return instance


class LevelTeamFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTeamFeedback
        fields = '__all__'
        
    def create(self, validated_data):
        levelteamfeedback = LevelTeamFeedback.objects.create(
            **validated_data)
        return levelteamfeedback

    def update(self, instance, validated_data):
        instance.stars = validated_data.get('stars', instance.stars)
        instance.feedback = validated_data.get('feedback', instance.feedback)
        instance.save()
        return instance
