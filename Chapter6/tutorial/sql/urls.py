from django.urls import path

from sql import views

urlpatterns = [
    path('get',views.PetViewSet.as_view())
]