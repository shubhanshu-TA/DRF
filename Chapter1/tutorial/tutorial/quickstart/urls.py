from django.urls import path,include
from quickstart import views

urlpatterns = [
    path('',views.index)
]
