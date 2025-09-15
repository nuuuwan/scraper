import os
import shutil
import unittest
from functools import cached_property
from unittest.mock import patch

from pdf_scraper import AbstractDoc
from utils_future import WWW


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
        return "http://example.com/test.pdf"


class TestCase(unittest.TestCase):
    def test_abstract(self):
        doc = AbstractDoc(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_pdf="http://example.com/test.pdf",
            url_metadata="http://example.com/test.json",
        )
        with self.assertRaises(NotImplementedError):
            _ = doc.remote_data_url

    def test_base(self):
        doc = DummyDoc()
        self.assertEqual(
            doc.dir_doc_extended_without_base,
            os.path.join(
                "data", "dummy", "2020s", "2023", "2023-10-01-1234567890"
            ),
        )

        self.assertEqual(
            doc.get_dir_extended_root(),
            os.path.join("..", "pdf_scraper_data"),
        )

        self.assertEqual(
            doc.dir_doc_extended,
            os.path.join(
                doc.get_dir_extended_root(),
                doc.dir_doc_extended_without_base,
            ),
        )

        self.assertEqual(
            doc.pdf_path,
            os.path.join(doc.dir_doc_extended, "en.pdf"),
        )

    def test_post_write(self):

        mock_dir_root = os.path.join("tests", "output", "data_parent")
        shutil.rmtree(mock_dir_root, ignore_errors=True)
        mock_dir_extended_root = os.path.join(
            "tests", "output", "extended_data_parent"
        )
        shutil.rmtree(mock_dir_extended_root, ignore_errors=True)

        def mock_download_binary(local_path):
            shutil.copy(
                os.path.join("tests", "input", "test.pdf"),
                local_path,
            )

        with patch.object(
            DummyDoc,
            "get_dir_root",
            return_value=mock_dir_root,
        ), patch.object(
            DummyDoc,
            "get_dir_extended_root",
            return_value=mock_dir_extended_root,
        ), patch.object(
            WWW, "download_binary", side_effect=mock_download_binary
        ):
            doc = DummyDoc()
            doc.write()

            self.assertFalse(doc.has_pdf)
            self.assertEqual(doc.extract_blocks(), None)
            self.assertEqual(len(doc.get_text()), 0)

            doc.scrape_extended_data()
            self.assertTrue(doc.has_pdf)
            self.assertEqual(doc.get_total_file_size(), 18_435)
            self.assertEqual(len(doc.get_text()), 39)
