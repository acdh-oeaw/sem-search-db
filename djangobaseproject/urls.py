from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from archiv import api_views

router = routers.DefaultRouter()
router.register(r"collections", api_views.CollectionViewset)
router.register(r"textsnippets", api_views.TextSnippetViewset)
router.register(r"questions", api_views.UserInputViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("browsing/", include("browsing.urls", namespace="browsing")),
    path("", include("webpage.urls", namespace="webpage")),
]
handler404 = "webpage.views.handler404"
