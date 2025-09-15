from abc import ABC, abstractmethod
from typing import Generator

from utils_future import WWW

from pdf_scraper.AbstractDataPage import AbstractDataPage


class AbstractHomePage(WWW, ABC):

    @abstractmethod
    def gen_data_pages(self) -> Generator[AbstractDataPage, None, None]:
        pass
