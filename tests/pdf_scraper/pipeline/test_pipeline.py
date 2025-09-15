import unittest

from pdf_scraper import AbstractDoc, AbstractHomePage, Pipeline


class DummyHomePage(AbstractHomePage):
    def __init__(self):
        super().__init__("https://example.com")

    def gen_data_pages(self):
        return []


class TestCase(unittest.TestCase):
    def test_pipeline_run(self):
        pipeline = Pipeline(
            home_page_class=DummyHomePage,
            doc_class=AbstractDoc,
        )
        pipeline.run(max_dt=1)
