import os
from functools import cached_property
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import File, Log, hashx

log = Log('Scraper')


class BaseScraper:
    HASH_ID_LENGTH = 8
    DOMAIN_ID_MAX_LENGTH = 32

    def __init__(self, url):
        self.url = url

    @property
    def domain_id(self):
        domain_id = urlparse(self.url).netloc[: self.DOMAIN_ID_MAX_LENGTH]
        domain_id = domain_id.replace('.github', '.gh')
        return domain_id

    @property
    def dir_domain(self):
        return f'data/scraper-{self.domain_id}'

    def make_dir_domain(self):
        if not os.path.exists(self.dir_domain):
            log.debug(f'Made directory {self.dir_domain}')
            os.makedirs(self.dir_domain)

    @property
    def hash_id(self):
        return hashx.md5(self.url)[: self.HASH_ID_LENGTH]

    @property
    def local_path(self):
        base_name = f'{self.dir_domain}/{self.hash_id}'
        if self.url.endswith('.pdf'):
            return f'{base_name}.pdf'
        return f'{base_name}.htm'

    @property
    def local_file(self):
        return File(self.local_path)

    def load_html(self):
        return self.local_file.read()

    def store_html(self):
        log.debug(f'Scraping {self.url}...')

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        html = driver.page_source
        driver.close()
        driver.quit()
        html_size = len(html)

        self.make_dir_domain()
        self.local_file.write(html)
        log.debug(f'Scraped {self.url} to {self.local_path} ({html_size:,}B)')

        return html

    @cached_property
    def html(self):
        if self.local_file.exists:
            log.debug(f'{self.local_path} already exists.')
            return self.load_html()
        return self.store_html()

    @property
    def soup(self):
        return BeautifulSoup(self.html, 'html.parser')

    def download_binary(self):
        if self.local_file.exists:
            log.debug(f'{self.local_path} already exists.')
            return self.local_file.path

        self.make_dir_domain()

        try:
            os.system(f'wget -O "{self.local_path}" "{self.url}"')
            file_size = os.path.getsize(self.local_path)
            log.debug(
                f'Downloaded {self.url} to {self.local_path} ({file_size:,}B)'
            )
        except BaseException as e:
            log.error(e)
            log.error(f'Could not download {self.url}')
            return None

        return self.local_file.path
