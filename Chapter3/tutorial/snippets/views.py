from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@csrf_exempt
def snippet_list(request):
    if request.method =='GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets,many = True)
        return JsonResponse(serializer.data, safe= False)
