from utils import Log

from scraper.LinkScraper import LinkScraper

log = Log('Spider')


class Spider(LinkScraper):
    @staticmethod
    def is_spiderable_url(url):
        ext = url.split('.')[-1]
        return all(['http' in url, ext not in ['pdf', 'jpg', 'png', 'gif']])

    def get_expanded_urls(self, approx_limit=10):
        urls = self.urls
        if len(urls) < approx_limit:
            for url in self.urls:
                if not self.is_spiderable_url(url):
                    continue

                urls += Spider(url).get_expanded_urls(
                    approx_limit - len(urls)
                )

                if len(urls) >= approx_limit:
                    break

        log.debug(f'Found {len(urls)} PDF URLs in {self.url}.')
        return urls
