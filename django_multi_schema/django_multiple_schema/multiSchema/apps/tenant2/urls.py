from apps.tenant2.views import LanguageList, LanguageDetail
from django.urls import path


urlpatterns = [
    path("languages", LanguageList.as_view()),
    path(
        "languages/<int:language_id>/",
        LanguageDetail.as_view(),
    ),
]
