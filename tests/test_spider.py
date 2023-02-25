from unittest import TestCase

from scraper import Spider
from tests.test_base_scraper import TEST_URL, TEST_URL_PDF


class TestSpider(TestCase):
    def test_expanded_pdf_urls(self):
        spider = Spider(TEST_URL)
        expanded_urls = spider.get_expanded_urls(max_depth=0)
        self.assertEqual(
            expanded_urls,
            [TEST_URL_PDF],
        )
