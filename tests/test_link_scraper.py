from unittest import TestCase

from scraper import LinkScraper
from tests.test_base_scraper import TEST_URL


class TestLinkScraper(TestCase):
    def test_urls(self):
        urls = LinkScraper(TEST_URL).urls
        self.assertEqual(len(urls), 44)
        self.assertEqual(urls[0], '#')
