from apps.common.views import (
    LanguageDetail,
    LanguageList,
    LanRegDetail,
    RegionDetail,
    TenantDetail,
    LanRegDfDetail,
)
from django.urls import path

urlpatterns = [
    path("languages", LanguageList.as_view()),
    path(
        "languages/<int:language_id>/",
        LanguageDetail.as_view(),
    ),
    path("regions/<int:region_id>/", RegionDetail.as_view()),
    path("tenants/<int:tenant_id>/", TenantDetail.as_view()),
    path("lanreg/<int:region_id>/", LanRegDetail.as_view()),
    path("lanregdf/<int:region_id>/", LanRegDfDetail.as_view()),
]
