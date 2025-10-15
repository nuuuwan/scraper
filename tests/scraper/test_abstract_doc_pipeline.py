import os
import random
import shutil
import unittest
from unittest.mock import patch

from scraper import AbstractDoc

DIR_TEST_ABSTRACT_DOC = os.path.join(
    "tests", "output", "test_abstract_doc_pipeline"
)


class DummyDoc(AbstractDoc):

    @classmethod
    def gen_docs(cls):
        for i in range(0, 101):
            year = 2000 + i
            month = i % 12 + 1
            day = i % 28 + 1
            yield DummyDoc(
                num=f"{i:04d}",
                date_str=f"{year:04d}-{month:02d}-{day:02d}",
                description="Test Document",
                url_metadata="http://mock.com/doc.html",
                lang="en",
            )

    @classmethod
    def get_main_branch_dir_root(cls):
        return os.path.join(DIR_TEST_ABSTRACT_DOC, "data_root")

    @classmethod
    def get_data_branch_dir_root(cls):
        return os.path.join(DIR_TEST_ABSTRACT_DOC, "extended_data_root")


class TestCase(unittest.TestCase):
    def test_run_pipeline(self):
        shutil.rmtree(DummyDoc.get_data_branch_dir_root(), ignore_errors=True)
        DummyDoc.run_pipeline(max_dt=0.00001)
        DummyDoc.run_pipeline(max_dt=600)
        self.assertEqual(len(DummyDoc.list_all()), 101)
