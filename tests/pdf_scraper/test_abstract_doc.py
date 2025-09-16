import unittest

from pdf_scraper import AbstractDoc


class DummyDoc(AbstractDoc):
    def __init__(self):
        super().__init__(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_pdf="http://example.com/test.pdf",
            url_metadata="http://example.com/test.json",
        )

    @classmethod
    def gen_docs(cls):
        yield DummyDoc()


class TestCase(unittest.TestCase):

    def test_pipeline(self):
        DummyDoc.run_pipeline(max_dt=0.001)
