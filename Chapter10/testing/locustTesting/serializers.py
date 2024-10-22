from rest_framework import serializers
from .models import Comment, Post

class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.Serializer):
    class Meta:
            model = Post
            fields = '__all__'