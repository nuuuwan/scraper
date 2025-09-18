import os
import shutil
import unittest
from unittest.mock import patch

from datasets import Dataset

from scraper import AbstractPDFDoc
from utils_future import WWW

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
        return os.path.join(DIR_TEST_PIPELINE, "data_root")

    @classmethod
    def get_data_branch_dir_root(cls):
        return os.path.join(DIR_TEST_PIPELINE, "extended_data_root")


class TestCase(unittest.TestCase):

    def test_pipeline(self):
        shutil.rmtree(DIR_TEST_PIPELINE, ignore_errors=True)

        mock_pdf_path = os.path.join("tests", "input", "test.pdf")
        self.assertTrue(os.path.exists(mock_pdf_path))

        def mock_download_binary(local_path):
            shutil.copyfile(mock_pdf_path, local_path)

        with patch.object(
            WWW, "download_binary", side_effect=mock_download_binary
        ), patch.object(
            Dataset, "push_to_hub", return_value="mock_dataset_id"
        ):

            DummyDoc.run_pipeline(max_dt=0.001)
            DummyDoc.run_pipeline(max_dt=10)

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
