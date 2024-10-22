from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from movie import views

urlpatterns = [
    path('movie/',views.MovieList.as_view()),
    path('movie/<int:pk>/', views.MovieDetail.as_view())
]

