import os
import shutil
import unittest

from scraper import AbstractPDFDoc

DIR_TEST_PIPELINE = os.path.join("tests", "output", "test_abstract_pdf_doc")


class TestPDFDoc(AbstractPDFDoc):
    @classmethod
    def gen_docs(cls):
        for i in range(0, 5):
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
                + "/tests/input/test-with-tabel.pdf",
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
        doc = TestPDFDoc.gen_docs().__next__()
        self.assertEqual(doc.num, "0000")
        self.assertFalse(doc.has_pdf)

    def test_pipeline(self):
        shutil.rmtree(DIR_TEST_PIPELINE, ignore_errors=True)
        TestPDFDoc.run_pipeline(max_dt=1)
