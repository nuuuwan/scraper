import os
import unittest

from pdf_scraper import AbstractDoc


class TestDoc(AbstractDoc):
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
        test_doc = TestDoc()
        self.assertEqual(test_doc.doc_class_label(), "test")
        self.assertEqual(test_doc.doc_class_pretty_label(), "Test")
        self.assertEqual(
            test_doc.doc_class_description(),
            "A collection of Test documents.",
        )
        self.assertEqual(
            test_doc.get_dir_docs_root(), os.path.join("data", "test")
        )
        self.assertEqual(test_doc.num_short, "1234567890")
        self.assertEqual(test_doc.doc_id, "2023-10-01-1234567890")
        self.assertEqual(test_doc.decade, "2020s")
        self.assertEqual(test_doc.year, "2023")
        self.assertEqual(test_doc.year_and_month, "2023-10")

    def test_num_short_long(self):
        test_doc = TestDoc()
        test_doc.num = test_doc.num * 40
        self.assertEqual(
            test_doc.num_short,
            "12345678901234567890123-e92dc0f9",
        )
