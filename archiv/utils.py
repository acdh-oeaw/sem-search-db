import re

import llama_cpp
import numpy as np

from archiv.models import TextSnippet

client = llama_cpp.Llama(
    model_path="llama/models/model.gguf", embedding=True, verbose=False
)


def process_vrt_file(filepath):
    """
    Extract first tab-separated field from lines inside <s></s> tags.
    Join with spaces, except when a token is preceded by <g/>, then no space.
    Capture chapter ID and LandingPageURI and add to each sentence.
    """
    with open(filepath, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    results = []
    in_sentence = False
    tokens = []  # List of (token, preceded_by_g) tuples
    current_chapter_id = None
    current_chapter_uri = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check for chapter tag
        if line.startswith("<chapter"):
            # Extract ID and LandingPageURI
            id_match = re.search(r'ID="([^"]*)"', line)
            uri_match = re.search(r'LandingPageURI="([^"]*)"', line)
            current_chapter_id = id_match.group(1) if id_match else None
            current_chapter_uri = uri_match.group(1) if uri_match else None

        if line == "<s>":
            in_sentence = True
            tokens = []
        elif line == "</s>":
            in_sentence = False
            if tokens:
                # Build sentence string from tokens
                sentence_text = ""
                for j, (token, preceded_by_g) in enumerate(tokens):
                    if j == 0:
                        sentence_text = token
                    else:
                        if preceded_by_g:
                            sentence_text += token  # No space
                        else:
                            sentence_text += " " + token

                # Add chapter metadata
                if current_chapter_id and current_chapter_uri:
                    results.append(
                        f"{current_chapter_id}\t{current_chapter_uri}\t{sentence_text}"
                    )
                else:
                    results.append(sentence_text)
        elif (
            in_sentence
            and line
            and not line.startswith("<")
            and not line.endswith("/>")
        ):
            # Extract first tab-separated field
            first_field = line.split("\t")[0]

            # Check if previous non-empty line is <g/>
            prev_line_idx = i - 1
            while prev_line_idx >= 0 and not lines[prev_line_idx].strip():
                prev_line_idx -= 1

            is_preceded_by_g = (
                prev_line_idx >= 0 and lines[prev_line_idx].strip() == "<g/>"
            )

            tokens.append((first_field, is_preceded_by_g))

        i += 1

    return results


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
