import time
from datetime import timedelta

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
            default="__all__",
            help="Name of the collection to vectorize snippets for.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="If set, update existing vectors.",
        )

    def handle(self, *args, **options):
        start_time = time.time()
        collection_name = options.get("collection") or "TestCollection"
        update_flag = options.get("update", False)
        if collection_name == "__all__":
            items = TextSnippet.objects.all()
        else:
            col = Collection.objects.filter(title=collection_name)
            items = TextSnippet.objects.filter(collection__in=col)

        if not update_flag:
            items = items.filter(vectorized=False)
        for x in tqdm(items):
            try:
                vectorize(x, update=update_flag)
            except (BadRequestError, InternalServerError) as e:
                print(f"failed to process {x.content}, with text {len(x)} due to {e}")
        duration = time.time() - start_time
        print(f"done in {timedelta(seconds=int(duration))}")
