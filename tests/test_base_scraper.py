import os
from unittest import TestCase

from scraper import BaseScraper

TEST_URL = 'https://nuuuwan.github.io/scraper/example.htm'
TEST_URL_PDF = 'https://nuuuwan.github.io/scraper/example.pdf'


class TestBaseScraper(TestCase):
    def test_html(self):
        base_scraper = BaseScraper(TEST_URL)
        if base_scraper.local_file.exists:
            os.remove(base_scraper.local_path)
        html = base_scraper.html
        self.assertEqual(len(html), 217)

    def test_soup(self):
        soup = BaseScraper(TEST_URL).soup
        h1s = soup.find_all('h1')
        self.assertEqual(len(h1s), 1)
        self.assertEqual(h1s[0].text, 'Example')
