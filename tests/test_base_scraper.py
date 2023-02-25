import os
from unittest import TestCase

from scraper import BaseScraper

TEST_URL = os.path.join(
    'https://raw.githubusercontent.com',
    'nuuuwan/scraper/main/tests/example.htm',
)

TEST_URL_PDF = os.path.join(
    'https://raw.githubusercontent.com',
    'nuuuwan',
    'scraper/main/tests/example.pdf',
)


class TestBaseScraper(TestCase):
    def test_html(self):
        base_scraper = BaseScraper(TEST_URL)
        if base_scraper.local_file.exists:
            os.remove(base_scraper.local_path)
        html = base_scraper.html
        self.assertEqual(len(html), 440)
        print(html)
        self.assertEqual(html[:30], '<!docu')

    def test_soup(self):
        soup = BaseScraper(TEST_URL).soup
        h1s = soup.find_all('h1')
        self.assertEqual(len(h1s), 1)
        self.assertEqual(h1s[0].text, 'Example')
