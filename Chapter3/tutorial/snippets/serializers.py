from rest_framework import serializers

class SnippetSerializer(serializers.Serializer):
    code = serializers.CharField(style={'base_template': 'textarea.html'})
