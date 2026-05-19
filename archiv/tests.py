from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from archiv.models import Collection, TextSnippet

TEST_COLLECTION_TITLE = "TestCollection"

LINK_TO_SOURCE = "https://www.derstandard.at/story/3000000321035/lask-nach-turbulenten-sechs-jahrzehnten-wieder-an-der-spitze"


class ArchivTestCase(TestCase):
    def setUp(self):
        Collection.objects.get_or_create(title=TEST_COLLECTION_TITLE)
        col = Collection.objects.get_or_create(title=TEST_COLLECTION_TITLE)[0]
        samples = [
            {
                "collection": col,
                "content": "Klubchef Gruber ermöglichte Weg zurück nach oben, wird aber auch kritisch gesehen",
                "backlink": LINK_TO_SOURCE,
            },
            {
                "collection": col,
                "content": "LASK nach turbulenten sechs Jahrzehnten wieder an der Spitze",
                "backlink": LINK_TO_SOURCE,
            },
            {
                "collection": col,
                "content": "Club president Gruber paved the way for a return to the top, but he is also viewed critically",
                "backlink": LINK_TO_SOURCE,
                "lang_code": "eng",
            },
        ]

        for x in samples:
            item = TextSnippet.objects.create(**x)
            self.assertTrue("✗" in f"{item}")

    def test_01_create_embeddings(self):
        out = StringIO()
        call_command("create_embeddings", stdout=out)

        item = TextSnippet.objects.all().first()
        self.assertTrue("✓" in f"{item}")
        item.embedding = None
        item.save()
        self.assertTrue("✗" in f"{item}")
