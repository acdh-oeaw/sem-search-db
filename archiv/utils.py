import llama_cpp
import numpy as np

from archiv.models import TextSnippet


def vectorize(
    client: llama_cpp.Llama,
    model_object: TextSnippet,
    vector_field: str = "embedding",
    update=False,
):
    if model_object.content:
        if update or not isinstance(getattr(model_object, vector_field), np.ndarray):
            vector = client.create_embedding(
                model_object.content,
            )["data"][0]["embedding"]
            setattr(model_object, vector_field, vector)
            model_object.vectorized = True
            model_object.save()
