from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from archiv import api_views

router = routers.DefaultRouter()
router.register(r"collections", api_views.CollectionViewset)
router.register(r"textsnippets", api_views.TextSnippetViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("browsing/", include("browsing.urls", namespace="browsing")),
    path("", include("webpage.urls", namespace="webpage")),
]
handler404 = "webpage.views.handler404"
