from abc import ABC
from typing import Generator

from pdf_scraper.abstract_doc import AbstractDoc
from utils_future import WWW


class AbstractDataPage(WWW, ABC):

    def gen_docs(self) -> Generator[AbstractDoc, None, None]:
        pass
