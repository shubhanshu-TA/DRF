from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=10)
    password = serializers.CharField(required=True, allow_blank=False, max_length=10)