import os
from unittest import TestCase

from scraper import BaseScraper

TEST_URL = 'https://www.sltda.gov.lk/en/statistics'


class TestBaseScraper(TestCase):
    # @skip('content changes too often')
    def test_html(self):
        base_scraper = BaseScraper(TEST_URL)
        if base_scraper.local_file.exists:
            os.remove(base_scraper.local_path)
        html = base_scraper.html
        self.assertEqual(len(html), 132_992)

    # @skip('content changes too often')
    def test_soup(self):
        soup = BaseScraper(TEST_URL).soup
        divs = soup.find_all('div')
        self.assertEqual(len(divs), 128)
        self.assertEqual(divs[0].text[:10].strip(), 'Home')
