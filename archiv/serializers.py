from typing import TypedDict

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from archiv.models import Collection, TextSnippet, UserInput


class SimilarSnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    distance = serializers.FloatField()


class UserInputSerializer(serializers.HyperlinkedModelSerializer):
    most_similar_snippets = serializers.SerializerMethodField(
        label="similar snippets",
        help_text="Displays the n most similar snippets",
    )

    @extend_schema_field(SimilarSnippetSerializer(many=True))
    def get_most_similar_snippets(self, obj) -> list[SimilarSnippetDict]:
        request = self.context.get("request")
        if request is None:
            return []

        raw_n = request.query_params.get("most-similar")
        if raw_n in (None, ""):
            return []

        try:
            n = int(raw_n)
        except TypeError, ValueError:
            return []

        if n <= 0:
            return []

        n = min(n, 25)
        return [
            {"id": x.id, "content": x.content, "distance": x.distance}
            for x in obj.find_similar(amount=n)
        ]

    class Meta:
        model = UserInput
        fields = ["url", "content", "created_at", "embedding", "most_similar_snippets"]


class SimilarSnippetDict(TypedDict):
    id: int
    content: str
    distance: float


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "url",
            "title",
        ]


class TextSnippetSerializer(serializers.HyperlinkedModelSerializer):
    kwic = serializers.SerializerMethodField(
        label="KWIC", help_text="Displays search result with marked search term."
    )
    most_similar_snippets = serializers.SerializerMethodField(
        label="similar snippets",
        help_text="Displays the n most similar snippets",
    )

    def get_kwic(self, obj) -> str:
        return getattr(obj, "kwic", "")

    @extend_schema_field(SimilarSnippetSerializer(many=True))
    def get_most_similar_snippets(self, obj) -> list[SimilarSnippetDict]:
        request = self.context.get("request")
        if request is None:
            return []

        raw_n = request.query_params.get("most-similar")
        if raw_n in (None, ""):
            return []

        try:
            n = int(raw_n)
        except TypeError, ValueError:
            return []

        if n <= 0:
            return []

        n = min(n, 25)
        return [
            {"id": x.id, "content": x.content, "distance": x.distance}
            for x in obj.find_similar(amount=n)
        ]

    class Meta:
        model = TextSnippet
        fields = [
            "url",
            "vectorized",
            "collection",
            "lang_code",
            "content",
            "kwic",
            "most_similar_snippets",
        ]
