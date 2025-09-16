from abc import ABC
from typing import Generator

from pdf_scraper.abstract_doc import AbstractDoc


class AbstractDocGenerator(ABC):

    def gen_docs(self) -> Generator[AbstractDoc, None, None]:
        pass
