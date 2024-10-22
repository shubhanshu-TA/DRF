from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.Serializer):
    class Meta: 
        model = Pet
        fields = '__all__'
    
    # unit of work ---- creation of object
    def create(self, validated_data):
        instance = Pet.objects.create(**validated_data)
        return instance
