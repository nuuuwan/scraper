import os
import shutil
import unittest
from functools import cached_property
from unittest.mock import patch

from pdf_scraper import AbstractDoc, AbstractDocGenerator, Pipeline
from utils_future import WWW


class DummyDoc(AbstractDoc):

    @classmethod
    def get_dir_root(cls) -> str:
        return os.path.join("tests", "output", "data_parent")

    @classmethod
    def get_dir_extended_root(cls) -> str:
        return os.path.join("tests", "output", "extended_data_parent")

    @cached_property
    def remote_data_url(self) -> str:
        return self.url_pdf


class DummyDataPage(AbstractDocGenerator):
    def gen_docs(self):
        dummy_doc = DummyDoc(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_pdf="http://example.com/test.pdf",
            url_metadata="http://example.com/test.json",
        )

        yield dummy_doc


class TestCase(unittest.TestCase):
    def test_pipeline_run(self):
        def mock_download_binary(local_path):
            shutil.copy(
                os.path.join("tests", "input", "test.pdf"),
                local_path,
            )

        with patch.object(
            WWW, "download_binary", side_effect=mock_download_binary
        ):
            pipeline = Pipeline(
                data_page_class=DummyDataPage,
                doc_class=DummyDoc,
            )
            pipeline.run(max_dt=0.0001)
            pipeline.run(max_dt=10)

            doc_list = DummyDoc.list_all()
            self.assertEqual(len(doc_list), 1)
            self.assertTrue(doc_list[0].has_pdf)
