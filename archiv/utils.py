import llama_cpp
import numpy as np

from archiv.models import TextSnippet

client = llama_cpp.Llama(
    model_path="llama/models/model.gguf", embedding=True, verbose=False
)


def vectorize(
    model_object: TextSnippet,
    vector_field: str = "embedding",
    update=False,
    client=client,
):
    if model_object.content:
        if update or not isinstance(getattr(model_object, vector_field), np.ndarray):
            vector = client.create_embedding(
                model_object.content,
            )["data"][0]["embedding"]
            setattr(model_object, vector_field, vector)
            model_object.save()
