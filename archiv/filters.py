from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from django.db.utils import ProgrammingError
from django_filters import rest_framework as django_filters

from archiv.models import Collection, TextSnippet

START_SELECTOR = "<mark>"
END_SELECTOR = "</mark>"


class TextSnippetListFilter(django_filters.FilterSet):
    ft_search = django_filters.CharFilter(
        field_name="vector_column",
        method="search_fulltext",
        label="Full-text search",
    )

    def search_fulltext(self, queryset, field_name, value):
        search_type = "websearch"
        search_term = value
        if value and value.endswith("*"):
            search_type = "raw"
            search_term = value.replace("*", ":*")
            query = SearchQuery(search_term, config="german", search_type=search_type)
            qs = (
                queryset.filter(vector_column=query)
                .annotate(
                    kwic=SearchHeadline(
                        "content",
                        query,
                        config="german",
                        start_sel=START_SELECTOR,
                        stop_sel=END_SELECTOR,
                    )
                )
                .annotate(rank=SearchRank("content", query))
                .order_by("-rank")
            )
            try:
                qs
            except ProgrammingError:
                return queryset
        else:
            query = SearchQuery(value, config="german", search_type=search_type)
            qs = (
                queryset.filter(vector_column=query)
                .annotate(
                    kwic=SearchHeadline(
                        "content",
                        query,
                        config="german",
                        start_sel=START_SELECTOR,
                        stop_sel=END_SELECTOR,
                    )
                )
                .annotate(rank=SearchRank("content", query))
                .order_by("-rank")
            )
        return qs

    class Meta:
        model = TextSnippet
        fields = [
            "id",
            "content",
            "lang_code",
            "collection",
            "vectorized",
        ]


class CollectionListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
        ]
