import unittest

from pdf_scraper import AbstractDoc


class DummyDoc(AbstractDoc):
    def __init__(self):
        super().__init__(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_pdf="http://example.com/test.pdf",
            url_metadata="http://example.com/test.json",
        )


class TestCase(unittest.TestCase):
    def test_method(self):
        doc = DummyDoc()
        self.assertEqual(doc.doc_class_label(), "dummy")
        self.assertEqual(doc.doc_class_pretty_label(), "Dummy")
        self.assertEqual(
            doc.doc_class_description(),
            "A collection of Dummy documents.",
        )

        self.assertEqual(doc.num_short, "1234567890")
        self.assertEqual(doc.doc_id, "2023-10-01-1234567890")
        self.assertEqual(doc.decade, "2020s")
        self.assertEqual(doc.year, "2023")
        self.assertEqual(doc.year_and_month, "2023-10")

    def test_num_short_long(self):
        doc = DummyDoc()
        doc.num = doc.num * 40
        self.assertEqual(
            doc.num_short,
            "12345678901234567890123-e92dc0f9",
        )
