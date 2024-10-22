from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your views here.

class UserView(APIView):

    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)


class TokenView(APIView):

    def get(self,request):
        user = User.objects.create_user(username = request.data['user'],password=request.data['pass'],email=request.data['email'])
        user.save()
        token = Token.objects.create(user=user)
        return Response(token.key)


