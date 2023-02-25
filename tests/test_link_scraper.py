from unittest import TestCase

from scraper import LinkScraper
from tests.test_base_scraper import TEST_URL, TEST_URL_PDF


class TestLinkScraper(TestCase):
    def test_urls(self):
        urls = LinkScraper(TEST_URL).urls
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0], TEST_URL_PDF)
