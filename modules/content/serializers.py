from .models import *
from rest_framework import serializers


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


class ContentSerializer(serializers.ModelSerializer):
    files = FileSerializer(read_only=True, many=True)
    problems = ProblemSerializer(read_only=True, many=True)
    video = VideoSerializer(read_only=True, many=True)

    class Meta:
        model = Content
        fields = ('files', 'video', 'problems')
