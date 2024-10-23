from movie.models import Movie
from movie.serializers import MovieSerializer
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class MovieList(APIView):

    def get(self,request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)



class MovieDetail(APIView):
    def get_object(self,pk):
        try: 
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
