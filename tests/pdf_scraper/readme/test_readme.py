import os
import unittest
from unittest.mock import patch

from pdf_scraper import AbstractDoc, AbstractHomePage, ReadMe


class TestCase(unittest.TestCase):
    def test_empty(self):
        readme = ReadMe(
            home_page_class=AbstractHomePage, doc_class=AbstractDoc
        )
        readme.build()

    def test_full(self):
        mock_dir_root = os.path.join("tests", "output", "data_parent")
        with patch.object(
            AbstractDoc,
            "list_all",
            return_value=[
                AbstractDoc(
                    num="1234567890",
                    date_str="2023-10-01",
                    description="Test document",
                    url_pdf="http://example.com/doc.pdf",
                    url_metadata="http://example.com/metadata.json",
                )
            ],
        ), patch.object(
            AbstractDoc, "get_dir_root", return_value=mock_dir_root
        ):
            readme = ReadMe(
                home_page_class=AbstractHomePage, doc_class=AbstractDoc
            )
            self.assertEqual(len(readme.doc_list), 1)
            readme.build()
