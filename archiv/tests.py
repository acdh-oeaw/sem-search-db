from io import StringIO

from django.core.management import call_command
from django.test import Client, TestCase

from archiv.models import Collection, TextSnippet

client = Client()

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
            TextSnippet.objects.create(**x)

    def get_list_view_endpoints(self):
        response = client.get("/api/")
        return list(response.json().values())

    def test_01_create_embeddings(self):
        out = StringIO()
        call_command("create_embeddings", stdout=out)

        item = TextSnippet.objects.all().first()
        self.assertTrue("✓" in f"{item}")
        item.embedding = None
        item.save()
        self.assertTrue("✗" in f"{item}")

    def test_02_generic_api_endpoints(self):

        endpoints = [x for x in self.get_list_view_endpoints()]
        for x in endpoints:
            response = client.get(x)
            self.assertEqual(
                response.status_code,
                200,
                f"Expected 200 for {x}, got {response.status_code}",
            )
            data = response.json()
            self.assertTrue("results" in data.keys())

        self.assertTrue(
            TextSnippet.objects.all().count() == 3,
            msg=f"Should be three but go {TextSnippet.objects.all().count()}",
        )

    def test_03_kwic_filter(self):
        search_term = "LASK"
        url = f"/api/textsnippets/?ft_search={search_term}"
        response = client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200 for {url}, got {response.status_code}",
        )
        data = response.json()
        kwic = data["results"][0]["kwic"]
        self.assertTrue(f"<mark>{search_term}</mark>" in kwic)

        search_term = "Klubch*"
        url = f"/api/textsnippets/?ft_search={search_term}"
        response = client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200 for {url}, got {response.status_code}",
        )
        data = response.json()
        kwic = data["results"][0]["kwic"]
        self.assertTrue("<mark>Klubchef</mark>" in kwic)
