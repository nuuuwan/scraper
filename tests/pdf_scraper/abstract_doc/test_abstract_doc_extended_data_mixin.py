import os
import shutil
import unittest
from functools import cached_property

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

    @cached_property
    def remote_data_url(self) -> str:
        return None


class TestCase(unittest.TestCase):
    def test_base(self):
        doc = DummyDoc()
        self.assertEqual(
            doc.dir_doc_extended_without_base,
            os.path.join(
                "data", "dummy", "2020s", "2023", "2023-10-01-1234567890"
            ),
        )

        self.assertEqual(
            doc.get_dir_doc_extended_root(),
            os.path.join("..", "pdf_scraper_data"),
        )

        self.assertEqual(
            doc.dir_doc_extended,
            os.path.join(
                doc.get_dir_doc_extended_root(),
                doc.dir_doc_extended_without_base,
            ),
        )

        self.assertEqual(
            doc.pdf_path,
            os.path.join(doc.dir_doc_extended, "en.pdf"),
        )

    def test_post_write(self):
        DummyDoc.get_dir_docs_root = lambda: os.path.join(
            "tests", "output", "data"
        )
        shutil.rmtree(DummyDoc.get_dir_docs_root(), ignore_errors=True)
        doc = DummyDoc()
        doc.write()

        DummyDoc.get_dir_doc_extended_root = lambda: os.path.join(
            "tests", "output", "data_extended"
        )
        shutil.rmtree(DummyDoc.get_dir_doc_extended_root(), ignore_errors=True)

        doc.scrape_extended_data()
