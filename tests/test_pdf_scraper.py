from unittest import TestCase

from scraper import PDFScraper
from tests.test_base_scraper import TEST_URL, TEST_URL_PDF


class TestPDFScraper(TestCase):
    def test_pdf_urls(self):
        scraper = PDFScraper(TEST_URL)
        self.assertEqual(
            scraper.pdf_urls[0],
            TEST_URL_PDF,
        )

    def test_download_all(self):
        scraper = PDFScraper(TEST_URL)
        scraper.download_all()
