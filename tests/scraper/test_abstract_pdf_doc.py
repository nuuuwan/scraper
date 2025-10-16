import os
import shutil
import unittest
from unittest.mock import patch

from scraper import AbstractPDFDoc, GlobalReadMe

DIR_TEST_PIPELINE = os.path.join("tests", "output", "test_abstract_pdf_doc")


class TestPDFDoc(AbstractPDFDoc):
    @classmethod
    def gen_docs(cls):
        for i in range(0, 1):
            year = 2000 + i
            month = (i % 12) + 1
            day = (i % 28) + 1
            yield TestPDFDoc(
                num=f"{i:04d}",
                date_str=f"{year:04d}-{month:02d}-{day:02d}",
                description="Test Document",
                url_metadata="http://mock.com/mock.html",
                url_pdf="https://github.com/nuuuwan"
                + "/scraper/raw/refs/heads/main"
                + "/tests/input/test-with-table.pdf",
                lang="en",
            )

    @classmethod
    def get_main_branch_dir_root(cls):
        return os.path.join(DIR_TEST_PIPELINE, "main_branch")

    @classmethod
    def get_data_branch_dir_root(cls):
        return os.path.join(DIR_TEST_PIPELINE, "data_branch")


class TestCase(unittest.TestCase):

    def test_init(self):
        shutil.rmtree(DIR_TEST_PIPELINE, ignore_errors=True)
        doc = next(TestPDFDoc.gen_docs())
        self.assertEqual(doc.num, "0000")
        self.assertFalse(doc.has_pdf)

    def test_get_tables(self):
        pdf_path = os.path.join("tests", "input", "test-with-table.pdf")
        tables = TestPDFDoc.get_tables(pdf_path)
        self.assertEqual(len(tables), 1)

    def test_pipeline(self):
        shutil.rmtree(DIR_TEST_PIPELINE, ignore_errors=True)
        doc = next(TestPDFDoc.gen_docs())
        self.assertFalse(doc.has_pdf)
        self.assertFalse(doc.has_blocks)
        self.assertFalse(doc.has_tabular)
        doc.extract_blocks()
        doc.extract_tabular()
        doc.extract_text()
        doc.get_text_from_block()

        with patch.object(
            GlobalReadMe,
            "PATH",
            os.path.join(DIR_TEST_PIPELINE, "README.md"),
        ):
            TestPDFDoc.run_pipeline(max_dt=1)

        doc = TestPDFDoc.list_all()[0]
        self.assertTrue(doc.has_pdf)
        self.assertTrue(doc.has_blocks)
        self.assertTrue(doc.has_tabular)
