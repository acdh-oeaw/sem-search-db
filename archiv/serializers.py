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
    most_similar_snippets = serializers.SerializerMethodField(
        label="similar snippets",
        help_text="Displays the n most similar snippets",
    )

    def get_kwic(self, obj) -> str:
        return getattr(obj, "kwic", "")

    def get_most_similar_snippets(self, obj) -> list:
        data = []
        request = self.context.get("request")
        n = int(request.query_params.get("most-similar", False))
        if n:
            try:
                n = int(n)
            except TypeError, ValueError:
                n = 5
            if n > 25:
                n = 25
            data = [
                {"id": x.id, "content": x.content, "distance": x.distance}
                for x in obj.find_similar(amount=n)
            ]

        return data

    class Meta:
        model = TextSnippet
        fields = [
            "url",
            "collection",
            "lang_code",
            "content",
            # "embedding",
            "kwic",
            "most_similar_snippets",
        ]
