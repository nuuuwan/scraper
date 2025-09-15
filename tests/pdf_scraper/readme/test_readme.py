import os
import unittest
from functools import cached_property
from unittest.mock import patch

from pdf_scraper import AbstractDoc, AbstractHomePage, ReadMe


class DummyHomePage(AbstractHomePage):
    def __init__(self):
        super().__init__("http://example.com")


class DummyDoc(AbstractDoc):
    @cached_property
    def remote_data_url(self) -> str:
        return "http://example.com/data.json"


class TestCase(unittest.TestCase):
    def test_empty(self):
        readme = ReadMe(
            home_page_class=AbstractHomePage, doc_class=AbstractDoc
        )
        self.assertEqual(len(readme.doc_list), 0)
        readme.build()

    def test_full(self):
        mock_dir_root = os.path.join("tests", "output", "data_parent")
        with patch.object(
            DummyDoc,
            "list_all",
            return_value=[
                DummyDoc(
                    num="1234567890",
                    date_str="2023-10-01",
                    description="Test document",
                    url_pdf="http://example.com/doc.pdf",
                    url_metadata="http://example.com/metadata.json",
                )
            ],
        ), patch.object(DummyDoc, "get_dir_root", return_value=mock_dir_root):
            readme = ReadMe(home_page_class=DummyHomePage, doc_class=DummyDoc)
            self.assertEqual(len(readme.doc_list), 1)
            readme.build()
