from rest_framework import serializers

from archiv.models import Collection, TextSnippet


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

    def get_kwic(self, obj) -> str:
        return getattr(obj, "kwic", "")

    class Meta:
        model = TextSnippet
        fields = [
            "url",
            "collection",
            "lang_code",
            "content",
            # "embedding",
            "kwic",
        ]
