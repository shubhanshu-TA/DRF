from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class TemplateView(APIView):
    
    def get(self, request):
        context = {
            'variable': 'value',
            # Add more context data as needed
        }
        return render(request, 'templates/template_name.html', context)
