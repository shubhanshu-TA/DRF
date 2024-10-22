
from django.urls import path

from authentication import views


urlpatterns = [
    path('allUsers/',views.UserView.as_view()),
    path('getToken/',views.TokenView.as_view())
]