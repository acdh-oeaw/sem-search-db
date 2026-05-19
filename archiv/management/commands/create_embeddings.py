import time
from datetime import timedelta

import llama_cpp
from django.core.management.base import BaseCommand
from openai import BadRequestError, InternalServerError
from tqdm import tqdm

from archiv.models import Collection, TextSnippet
from archiv.utils import vectorize


class Command(BaseCommand):
    help = "Vectorize text snippets for a given collection."

    def add_arguments(self, parser):
        parser.add_argument(
            "--collection",
            type=str,
            default="TestCollection",
            help="Name of the collection to vectorize snippets for.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="If set, update existing vectors.",
        )

    def handle(self, *args, **options):
        client = llama_cpp.Llama(model_path="llama/models/model.gguf", embedding=True)
        start_time = time.time()
        collection_name = options.get("collection") or "TestCollection"
        update_flag = options.get("update", False)
        col = Collection.objects.filter(title=collection_name)
        if update_flag:
            items = TextSnippet.objects.filter(collection__in=col)
        else:
            items = TextSnippet.objects.filter(collection__in=col).filter(
                vectorized=True
            )
        for x in tqdm(items):
            try:
                vectorize(client, x, update=update_flag)
            except (BadRequestError, InternalServerError) as e:
                print(f"failed to process {x.content}, with text {len(x)} due to {e}")
        duration = time.time() - start_time
        print(f"done in {timedelta(seconds=int(duration))}")
