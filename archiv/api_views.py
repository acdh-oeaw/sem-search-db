from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from archiv.filters import CollectionListFilter, TextSnippetListFilter
from archiv.models import Collection, TextSnippet
from archiv.serializers import CollectionSerializer, TextSnippetSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 25
    page_size_query_param = "page_size"


class CollectionViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filterset_class = CollectionListFilter


most_similar_param = OpenApiParameter(
    name="most-similar",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    required=False,
    description="Number of similar snippets to include per result (max 25).",
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            most_similar_param,
        ]
    ),
    retrieve=extend_schema(parameters=[most_similar_param]),
)
class TextSnippetViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = TextSnippet.objects.all()
    serializer_class = TextSnippetSerializer
    filterset_class = TextSnippetListFilter
