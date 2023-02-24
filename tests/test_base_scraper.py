import os
from unittest import TestCase

from scraper import BaseScraper

TEST_URL = 'https://www.sltda.gov.lk/en/statistics'


class TestBaseScraper(TestCase):
    def test_html(self):
        base_scraper = BaseScraper(TEST_URL)
        if base_scraper.local_html_file.exists:
            os.remove(base_scraper.local_html_path)
        html = base_scraper.html
        self.assertEqual(len(html), 132_992)

    def test_soup(self):
        soup = BaseScraper(TEST_URL).soup
        divs = soup.find_all('div')
        self.assertEqual(len(divs), 128)
        self.assertEqual(divs[0].text[:10].strip(), 'Home')
