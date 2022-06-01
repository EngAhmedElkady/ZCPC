from rest_framework import serializers
from .models import Round
# create round api


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'
        extra_kwargs = {
            'community': {'read_only': True},
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['community']=self.context['community']
        round = Round.objects.create(
            **validated_data)
        return round

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
