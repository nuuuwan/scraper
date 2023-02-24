from functools import cached_property

from scraper.BaseScraper import BaseScraper
from scraper.LinkScraper import LinkScraper


class PDFScraper(LinkScraper):
    @cached_property
    def pdf_urls(self):
        return [url for url in self.urls if url.endswith('.pdf')]

    def download_all(self):
        for url in self.pdf_urls:
            scraper = BaseScraper(url)
            scraper.download_binary()
