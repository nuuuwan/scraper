from unittest import TestCase

from scraper import Spider
from tests.test_base_scraper import TEST_URL


class TestSpider(TestCase):
    # def test_expanded_pdf_urls(self):
    #     spider = Spider(TEST_URL)
    #     expanded_urls = spider.get_expanded_urls(limit=1)
    #     self.assertEqual(
    #         expanded_urls,
    #         [TEST_URL_PDF],
    #     )

    #     expanded_urls = spider.get_expanded_urls(limit=20)
    #     self.assertEqual(
    #         expanded_urls,
    #         [TEST_URL_PDF],
    #     )

    # def test_spider_pdfs(self):
    #     spider = Spider(TEST_URL)
    #     pdf_file_paths = spider.spider_pdfs(limit=2)
    #     self.assertEqual(
    #         pdf_file_paths,
    #         ['/tmp/scraper-nuuuwan.gh.io/93683d24.pdf'],
    #     )

    def test_spider_tables(self):
        spider = Spider(TEST_URL)
        table_paths = spider.spider_tables(limit=2)
        self.assertEqual(
            table_paths,
            ['/tmp/scraper-nuuuwan.gh.io/93683d24.pdf.tables/table-00.tsv'],
        )
