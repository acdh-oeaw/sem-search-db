from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from archiv.filters import CollectionListFilter, TextSnippetListFilter
from archiv.models import Collection, TextSnippet
from archiv.serializers import CollectionSerializer, TextSnippetSerializer


class CustomPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 50
    page_size_query_param = "page_size"


class CollectionViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filterset_class = CollectionListFilter


class TextSnippetViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = TextSnippet.objects.all()
    serializer_class = TextSnippetSerializer
    filterset_class = TextSnippetListFilter
