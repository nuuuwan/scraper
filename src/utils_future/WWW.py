from functools import cached_property

import requests
import urllib3
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from utils import Log

log = Log("WebPage")

urllib3.disable_warnings(InsecureRequestWarning)


class WWW:
    TIMEOUT = 120

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"🌐 {self.url}"

    @cached_property
    def content(self):
        try:
            response = requests.get(
                self.url, timeout=self.TIMEOUT, verify=False
            )
            response.raise_for_status()
            content = response.text
            log.debug(f"[{self}] Opened. {len(content):,}B")
            return content
        except Exception as e:
            log.error(f"[{self}] Failed to open: {e}")
            return None

    @cached_property
    def soup(self):
        if not self.content:
            return None
        return BeautifulSoup(self.content, "html.parser")

    def download_binary(self, local_path):
        try:
            response = requests.get(self.url, timeout=self.TIMEOUT)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(response.content)
            log.info(f"Downloaded {self.url} to {local_path}")
        except Exception as e:
            log.error(f"Failed to download {self.url}: {e}")
            return
