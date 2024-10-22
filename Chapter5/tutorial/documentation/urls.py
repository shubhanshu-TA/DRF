
from django.urls import path

from documentation import views


urlpatterns = [
    path('all/',views.ProductViewSet.as_view())
]