import glob
import hashlib
import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import Collection, TextSnippet
from archiv.utils import process_vrt_file


class Command(BaseCommand):
    help = "Imports data from verticals"

    def add_arguments(self, parser):
        parser.add_argument(
            "--collection",
            type=str,
            default="",
            help="Name of the collection to vectorize snippets for.",
        )

    def handle(self, *args, **options):
        files = sorted(glob.glob("verticals/*.vrt"))
        black_list = [
            "abacus",
            "wiener-diarium",
            "bundesverfassung-oesterreich",
            "wibarab",
            "tunocent",
            "shawi",
        ]
        collection_name = options.get("collection") or "__all__"
        for x in files:
            file_name = os.path.split(x)[1].replace(".vrt", "")
            if collection_name == "__all__":
                pass
            elif collection_name == file_name:
                pass
            else:
                continue
            if file_name in black_list:
                print(f"skipping {x}")
                continue

            print(f"processing {x}")
            col = Collection.objects.get_or_create(title=file_name)[0]

            results = process_vrt_file(x)
            for y in tqdm(results, total=len(results)):
                col_name, backlink, content = y.split("\t")
                text_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                try:
                    TextSnippet.objects.get(text_hash=text_hash)
                    continue
                except ObjectDoesNotExist:
                    item, _ = TextSnippet.objects.get_or_create(
                        collection=col, content=content, backlink=backlink
                    )
            print("###########")
