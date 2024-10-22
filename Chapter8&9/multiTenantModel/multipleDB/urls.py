from django.urls import Path
from .apiviewss import PollViewSet, LoginViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register("polls", PollViewSet, base_name="polls")

urlpatterns = [
    path("login/", LoginViewSet.as_view(),name="login"),
    path("users/", UserCreate.as_view(),name="user_create"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(),name="polls_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(),name="polls_list"),
    ]

urlpatterns += router.urls
