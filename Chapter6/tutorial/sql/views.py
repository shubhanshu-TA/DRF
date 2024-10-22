from django.shortcuts import render
from .models import Pet
from .serializers import PetSerializer
from .respository import PetRepository
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.

class PetViewSet(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    respository = PetRepository()

    def get_queryset(self):
        breed = self.request.query_params.get('breed')
        print("breed-------",breed)
        if(breed):
            return self.respository.filter_by_breed(breed)
        return Pet.objects.all()  

