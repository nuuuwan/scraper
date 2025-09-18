import os
import unittest

from scraper import AbstractDoc

DIR_TEST_ABSTRACT_DOC = os.path.join("tests", "output", "test_abstract_doc")


class DummyDoc(AbstractDoc):
    def __init__(self):
        super().__init__(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            lang="en",
        )

    @classmethod
    def gen_docs(cls):
        yield DummyDoc()

    @classmethod
    def get_dir_root(cls):
        return os.path.join(DIR_TEST_ABSTRACT_DOC, "data_root")

    @classmethod
    def get_dir_extended_root(cls):
        return os.path.join(DIR_TEST_ABSTRACT_DOC, "extended_data_root")


class TestCase(unittest.TestCase):
    def test_gen_docs(self):
        self.assertEqual(AbstractDoc.gen_docs(), None)

    def test_num_short(self):
        doc = AbstractDoc(
            num="1234567890" * 10,
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            lang="en",
        )
        self.assertEqual(doc.num_short, "12345678901234567890123-49cb3608")

    def test_get_dir_root(self):
        self.assertEqual(AbstractDoc.get_dir_root(), ".")

    def test_get_dir_extended_root(self):
        self.assertEqual(
            AbstractDoc.get_dir_extended_root(), "../scraper_data"
        )
