from queue import Queue

from utils import Log

from scraper.LinkScraper import LinkScraper
from scraper.BaseScraper import BaseScraper
from scraper.PDFFile import PDFFile

log = Log('Spider')


class Spider:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def is_spiderable_url(url):
        ext = url.split('.')[-1]
        return all(['http' in url, ext not in ['pdf', 'jpg', 'png', 'gif']])

    def get_expanded_urls(self, limit=1):
        url_queue = Queue()
        visited_url_set = set()
        url_set = set()
        url_queue.put(self.url)

        while len(url_set) < limit and not url_queue.empty():
            url = url_queue.get()
            visited_url_set.add(url)
            if not self.is_spiderable_url(url):
                continue

            new_urls = LinkScraper(url).urls
            log.debug(f'Got {len(new_urls)} links from {url}.')

            for new_url in new_urls:
                if new_url in visited_url_set:
                    continue
                url_queue.put(new_url)
                if len(url_set) < limit:
                    url_set.add(new_url)

        log.info(f'Spidered {len(url_set)} URLs in {self.url} {limit=}.')
        return list(sorted(url_set))

    def spider_pdfs(self, limit=1):
        urls = self.get_expanded_urls(limit=limit)
        pdf_file_paths = []
        for url in urls:
            if PDFFile.is_remote_url_pdf(url):
                pdf_file_path = BaseScraper(url).download_binary()
                pdf_file_paths.append(pdf_file_path)
        return pdf_file_paths

    def spider_tables(self, limit=1):
        pdf_file_paths = self.spider_pdfs(limit=limit)
        table_paths = []
        for pdf_file_path in pdf_file_paths:
            pdf_file = PDFFile(pdf_file_path)
            table_paths += pdf_file.tables
        return table_paths
