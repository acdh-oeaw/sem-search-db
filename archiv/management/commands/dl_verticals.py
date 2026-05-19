import shutil
import subprocess
import tarfile
from pathlib import Path

from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    help = "Downloads and extracts verticals from an OCI image"

    def handle(self, *args, **options):
        IMG = "ghcr.io/acdh-oeaw/corpus-search/corpus-search"

        # Copy the image into an OCI archive.
        print(f"Copying {IMG} to tmp.tar...")
        subprocess.run(
            ["skopeo", "copy", f"docker://{IMG}", "oci-archive:tmp.tar:corpus-search"],
            check=True,
        )

        # Create tmp directory and extract tar
        print("Extracting tmp.tar...")
        Path("tmp").mkdir(exist_ok=True)
        with tarfile.open("tmp.tar", "r") as tar:
            tar.extractall("tmp")

        # Find the largest blob
        print("Finding largest blob...")
        blobs_dir = Path("tmp/blobs/sha256")
        largest_blob = max(blobs_dir.iterdir(), key=lambda p: p.stat().st_size)
        VERTICALS_BLOB = largest_blob.name
        print(f"Largest blob: {VERTICALS_BLOB}")

        print(f"Extracting {VERTICALS_BLOB}...")
        Path("tmp-verticals").mkdir(exist_ok=True)
        with tarfile.open(f"tmp/blobs/sha256/{VERTICALS_BLOB}", "r") as tar:
            tar.extractall("tmp-verticals")

        # Create verticals directory
        print("Creating verticals directory...")
        Path("verticals").mkdir(exist_ok=True)

        print("Copying *.yml and *.vrt files...")
        files = Path("tmp-verticals/var/lib/manatee/registry")
        count = 0
        for x in tqdm(files.rglob("*.yml")):
            shutil.copy(x, "verticals/")
            count += 1
        for x in tqdm(files.rglob("*.vrt")):
            shutil.copy(x, "verticals/")
            count += 1
        print(f"Copied {count} files to verticals/")

        print("Cleaning up...")
        shutil.rmtree("tmp", ignore_errors=True)
        shutil.rmtree("tmp-verticals", ignore_errors=True)
        Path("tmp.tar").unlink(missing_ok=True)

        print("Done!")
