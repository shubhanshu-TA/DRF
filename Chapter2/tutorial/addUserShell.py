from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

user = User(username="reviewer",password="drf")
user.save()
