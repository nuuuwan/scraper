from utils import Log

from scraper.LinkScraper import LinkScraper

log = Log('Spider')


class Spider(LinkScraper):
    def get_expanded_urls(self, max_depth=0):
        urls = self.urls
        if max_depth > 0:
            for url in self.urls:
                if 'http' not in url:
                    log.error(f'Not spidering {url}.')
                    continue
                
                if url.endswith('.pdf'):
                    log.debug(f'Not spidering PDF {url}.')
                    continue
                
                scraper = Spider(url)
                urls += scraper.get_expanded_urls(max_depth - 1)

        log.debug(f'Found {len(urls)} PDF URLs in {self.url}.')
        return urls
