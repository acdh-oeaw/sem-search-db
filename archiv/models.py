import hashlib

import numpy as np
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from pgvector.django import CosineDistance, HnswIndex, VectorField

from archiv.utils import client


class DateStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Collection(DateStampedModel):
    title = models.CharField(
        max_length=250, verbose_name="Titel", help_text="The collection's title"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.title


class TextSnippet(DateStampedModel):
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="snippets"
    )
    content = models.TextField(
        verbose_name="Content", help_text="The actual text content"
    )
    backlink = models.URLField(verbose_name="Link to source")
    lang_code = models.CharField(
        max_length=3,
        verbose_name="Language code",
        help_text="e.g. 'deu' or 'lat'",
        default="deu",
    )
    text_hash = models.CharField(
        max_length=64,
        db_index=True,
        editable=False,
    )
    embedding = VectorField(
        dimensions=768,
        verbose_name="Embedding (nomic-embed-text-v1.5)",
        blank=True,
        null=True,
    )
    vectorized = models.BooleanField(default=False, verbose_name="Embeddings exist")
    vector_column = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Text Snippet"
        verbose_name_plural = "Text Snippets"
        indexes = [
            GinIndex(fields=["vector_column"]),
            HnswIndex(
                name="textsnippetindex_nomic",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_l2_ops"],
            ),
        ]

    def __str__(self):
        if self.vectorized:
            vector = "✓"
        else:
            vector = "✗"
        return f"{vector}: {self.content[:25]}... ({self.collection}))"

    def save(self, *args, **kwargs):
        if self.content:
            self.text_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        if isinstance(self.embedding, np.ndarray) or isinstance(self.embedding, list):
            self.vectorized = True
        else:
            self.vectorized = False
        super().save(*args, **kwargs)

    def find_similar(
        self,
        vector_field: str = "embedding",
        collection_title: str = "__all__",
        amount: int = 3,
    ):
        amount = amount + 1
        if not self.vectorized:
            return TextSnippet.objects.none()
        if collection_title == "__all__":
            qs = TextSnippet.objects.all()
        else:
            col = Collection.objects.filter(title=collection_title)
            qs = TextSnippet.objects.filter(collection__in=col)
        qs = qs.exclude(**{f"{vector_field}__isnull": True})
        qs = qs.annotate(
            distance=CosineDistance(vector_field, getattr(self, vector_field))
        ).order_by("distance")[1:amount]
        return qs


class UserInput(DateStampedModel):
    content = models.CharField(
        max_length=500,
        verbose_name="Question",
        help_text="Input/Question provided by the user",
    )
    text_hash = models.CharField(
        max_length=64,
        db_index=True,
        editable=False,
    )
    embedding = VectorField(
        dimensions=768,
        verbose_name="Embedding (nomic-embed-text-v1.5)",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "User input"
        verbose_name_plural = "User inputs"
        indexes = [
            HnswIndex(
                name="userinput_nomic",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_l2_ops"],
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.text_hash:
            self.text_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        if not isinstance(self.embedding, np.ndarray) or isinstance(
            self.embedding, list
        ):
            vector = client.create_embedding(
                self.content,
            )["data"][0]["embedding"]
            self.embedding = vector
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.content[:50]}..."

    def find_similar(
        self,
        amount: int = 3,
    ):
        if self.embedding is None:
            return TextSnippet.objects.none()

        qs = TextSnippet.objects.exclude(embedding__isnull=True)
        qs = qs.annotate(distance=CosineDistance("embedding", self.embedding)).order_by(
            "distance"
        )[:amount]
        return qs
