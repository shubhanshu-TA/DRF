from django.shortcuts import render

# Create your views here.
import structlog
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response

logger = structlog.get_logger()
class ProductViewSet(APIView):
    """
    Returns a list of all Products
    """
    def get(self,request):
        queryset = Product.objects.all()
        logger.info('Listing products', user=request)
        serializer_class = ProductSerializer(queryset,many=True)
        return Response(serializer_class.data)
