from django.contrib import admin

from archiv.models import Collection, TextSnippet


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "text_snippet_count",
    ]

    def text_snippet_count(self, obj):
        return obj.snippets.count()

    text_snippet_count.short_description = "Text Snippet Count"


@admin.register(TextSnippet)
class TextSnippetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "collection",
        "lang_code",
        "vectorized",
        "content",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "collection",
        "vectorized",
        "lang_code",
    ]
