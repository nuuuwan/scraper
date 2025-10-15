import os
from dataclasses import dataclass
from functools import cached_property

import pandas as pd
from utils import WWW, Log

from scraper.abstract_doc.AbstractDoc import AbstractDoc
from scraper.abstract_doc.data_mixins.AbstractTabularMixin import (
    AbstractTabularMixin,
)

log = Log("AbstractExcelSpreadsheet")


@dataclass
class AbstractExcelSpreadsheet(AbstractTabularMixin, AbstractDoc):
    url_excel: str

    @cached_property
    def excel_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.xlsx")

    @property
    def has_excel(self) -> bool:
        return os.path.exists(self.excel_path)

    def download_excel(self):
        try:
            WWW(self.url_excel).download_binary(self.excel_path)
        except Exception as e:
            log.error(f"Failed to download Excel from {self.url_excel}: {e}")
            return

    # ----------------------------------------------------------------
    # Worksheets (extracted from Excel)
    # ----------------------------------------------------------------

    @staticmethod
    def open_excel(excel_path: str) -> pd.ExcelFile:
        engine = "openpyxl" if excel_path.endswith(".xlsx") else "xlrd"
        return pd.ExcelFile(excel_path, engine=engine)

    def extract_tabular(self):
        if not os.path.exists(self.excel_path):
            return
        excel = self.open_excel(self.excel_path)
        for i_sheet, sheet_name in enumerate(excel.sheet_names, 1):
            sheet_name_cleaned = sheet_name.replace("/", "_").replace(" ", "_")
            csv_path = os.path.join(
                self.dir_tabular,
                f"{i_sheet:02d}-{sheet_name_cleaned}.csv",
            )
            if os.path.exists(csv_path):
                continue

            df = excel.parse(sheet_name)
            os.makedirs(self.dir_tabular, exist_ok=True)
            df.to_csv(csv_path, index=False)
            log.info(f"Wrote {csv_path}")

    # ----------------------------------------------------------------
    # Scrape (ALL)
    # ----------------------------------------------------------------
    def scrape_extended_data_for_doc(self):
        if not self.has_excel:
            self.download_excel()

        self.scrape_extended_data_for_tabular_mixin()
