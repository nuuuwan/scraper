import os
from dataclasses import dataclass
from functools import cached_property

from utils import WWW

from scraper.abstract_doc.AbstractDoc import AbstractDoc


@dataclass
class AbstractExcelSpreadsheet(AbstractDoc):
    url_excel: str

    @cached_property
    def excel_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.xlsx")

    @property
    def has_excel(self) -> bool:
        return os.path.exists(self.excel_path)

    def download_excel(self):
        WWW(self.url_excel).download_binary(self.excel_path)
