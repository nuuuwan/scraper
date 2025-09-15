from abc import ABC, abstractmethod
from typing import Generator

from pdf_scraper.AbstractDataPage import AbstractDataPage
from utils_future import WWW


class AbstractHomePage(WWW, ABC):

    @abstractmethod
    def gen_data_pages(self) -> Generator[AbstractDataPage, None, None]:
        pass
