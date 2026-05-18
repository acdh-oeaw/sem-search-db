import numpy as np
from openai import OpenAI

from archiv.models import TextSnippet


def vectorize(
    client: OpenAI,
    model_object: TextSnippet,
    vector_field: str = "embedding_nomic",
    embedding_model_name: str = "nomic-embed-text",
    update=False,
):
    if model_object.content:
        if update or not isinstance(getattr(model_object, vector_field), np.ndarray):
            vector = (
                client.embeddings.create(
                    input=[model_object.content],
                    model=embedding_model_name,
                )
                .data[0]
                .embedding
            )
            setattr(model_object, vector_field, vector)
            model_object.save()
