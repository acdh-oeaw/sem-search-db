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
    kwic = serializers.SerializerMethodField()

    def get_kwic(self, obj):
        return getattr(obj, "kwic", None)

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
