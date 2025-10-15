import os
import shutil
import unittest
from unittest.mock import patch

from datasets import Dataset
from utils import WWW

from scraper import AbstractPDFDoc, GlobalReadMe

DIR_TEST_PIPELINE = os.path.join("tests", "output", "test_pipeline")


class DummyDoc(AbstractPDFDoc):
    def __init__(self):
        super().__init__(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            url_pdf="http://mock.com/doc.pdf",
            lang="en",
        )

    @classmethod
    def gen_docs(cls):
        yield DummyDoc()

    @classmethod
    def get_main_branch_dir_root(cls):
        return os.path.join(DIR_TEST_PIPELINE, "main_branch")

    @classmethod
    def get_data_branch_dir_root(cls):
        return os.path.join(DIR_TEST_PIPELINE, "data_branch")


class TestCase(unittest.TestCase):

    def test_pipeline(self):
        shutil.rmtree(DIR_TEST_PIPELINE, ignore_errors=True)
        mock_pdf_path = os.path.join("tests", "input", "test.pdf")
        self.assertTrue(os.path.exists(mock_pdf_path))

        def mock_download_binary(local_path):
            shutil.copyfile(mock_pdf_path, local_path)

        mock_summary_list = [
            {
                "repo_name": "mock_repo",
                "doc_class_label": "MockDoc",
                "doc_class_description": "A mock document class for testing.",
                "n_docs": 1,
                "n_pages": 1,
                "n_docs_with_pdfs": 1,
                "n_docs_with_text": 1,
                "n_docs_with_excel": 1,
                "dataset_size": 12345,
                "doc_class_emoji": "📄",
                "time_updated": "2024-10-01",
                "date_str_min": "2023-10-01",
                "date_str_max": "2023-10-01",
                "url_source_list": ["http://mock.com"],
                "url_data": "http://mock.com/data",
                "langs": ["en"],
                "url_chart": "http://mock.com/chart.png",
            }
        ]

        with patch.object(
            WWW, "download_binary", side_effect=mock_download_binary
        ), patch.object(
            Dataset, "push_to_hub", return_value="mock_dataset_id"
        ), patch.object(
            GlobalReadMe,
            "get_summary_list",
            return_value=mock_summary_list,
        ), patch.object(
            GlobalReadMe, "PATH", os.path.join(DIR_TEST_PIPELINE, "README.md")
        ):

            DummyDoc.run_pipeline(max_dt=0.001)
            DummyDoc.run_pipeline(max_dt=100)
            self.assertTrue(
                os.path.exists(DummyDoc.get_main_branch_dir_root())
            )
            self.assertTrue(
                os.path.exists(DummyDoc.get_data_branch_dir_root())
            )
            doc_list = DummyDoc.list_all()
            self.assertEqual(len(doc_list), 1)

            first_doc = doc_list[0]
            self.assertTrue(os.path.exists(first_doc.dir_doc))
            self.assertTrue(first_doc.has_pdf)

            text = first_doc.get_text()
            self.assertEqual(len(text), 96)
            self.assertEqual(text[:9], "Heading 1")

            blocks = first_doc.get_blocks()
            self.assertEqual(len(blocks), 6)

            url_metadata_set = DummyDoc.get_url_metadata_set()
            self.assertEqual(url_metadata_set, {"http://mock.com/doc.html"})
