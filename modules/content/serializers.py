from .models import *
from rest_framework import serializers


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("id", "description", "level", "get_community")


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
