
from rest_framework import serializers
from movie.models import Movie

class MovieSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance