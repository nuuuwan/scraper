import os
import tempfile
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

import camelot
from utils import WWW, File, JSONFile, Log, PDFFile

from scraper.abstract_doc import AbstractDoc
from scraper.abstract_doc.data_mixins.AbstractWorksheetsMixin import (
    AbstractWorksheetsMixin,
)

log = Log("AbstractPDFDoc")


@dataclass
class AbstractPDFDoc(AbstractDoc, ABC, AbstractWorksheetsMixin):
    url_pdf: str

    # ----------------------------------------------------------------
    # PDF
    # ----------------------------------------------------------------
    @cached_property
    def pdf_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.pdf")

    @property
    def has_pdf(self) -> bool:
        return os.path.exists(self.pdf_path)

    def download_pdf(self):
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=False
        ) as temp_pdf_f:
            temp_pdf_path = temp_pdf_f.name
            WWW(self.url_pdf).download_binary(temp_pdf_path)
            try:
                PDFFile(temp_pdf_path).compress(self.pdf_path)
            except Exception as e:
                log.warning(f"Failed to compress PDF from {self.url_pdf}: {e}")
                os.rename(temp_pdf_path, self.pdf_path)

    # ----------------------------------------------------------------
    # Blocks (Extracted from PDF)
    # ----------------------------------------------------------------
    @cached_property
    def blocks_path(self) -> str:
        return os.path.join(self.dir_doc, "blocks.json")

    @property
    def has_blocks(self) -> bool:
        return os.path.exists(self.blocks_path)

    def extract_blocks(self):
        if not self.has_pdf:
            return
        pdf_file = PDFFile(self.pdf_path)
        blocks = pdf_file.get_blocks()
        JSONFile(self.blocks_path).write(blocks)
        log.info(f"Wrote {self.blocks_path} ({len(blocks):,} blocks)")

    def get_blocks(self):
        return JSONFile(self.blocks_path).read()

    # ----------------------------------------------------------------
    # Worksheets (extracted from PDF)
    # ----------------------------------------------------------------

    def extract_worksheets(self):
        if not self.has_pdf:
            return
        tables = camelot.read_pdf(self.pdf_path, flavor="stream", pages="all")
        n_tables = len(tables)
        log.debug(f"Found {n_tables} tables in {self.pdf_path}")
        os.makedirs(self.dir_worksheets, exist_ok=True)
        tables.export(os.path.join(self.dir_worksheets, "table.csv"), f="csv")

    # ----------------------------------------------------------------
    # Text (From Blocks)
    # ----------------------------------------------------------------

    def get_text_from_block(self):
        if not self.has_pdf:
            return None
        blocks = self.get_blocks()
        text_list = [block["text"] for block in blocks if block["text"]]
        content = "\n\n".join(text_list)
        return content

    def get_text_all(self):
        return "\n".join(
            [
                "==== BLOCKS ==== ",
                "",
                self.get_text_from_block(),
                "",
                "==== WORKSHEETS ==== ",
                "",
                self.get_text_from_worksheets(),
                "",
            ]
        )

    def extract_text(self):
        if not self.has_pdf:
            return None
        File(self.text_path).write(self.get_text_all())
        log.info(f"Wrote {self.text_path}")

    # ----------------------------------------------------------------
    # All
    # ----------------------------------------------------------------
    def scrape_extended_data_for_doc(self):
        if not self.has_pdf:
            self.download_pdf()

        if self.has_pdf and not self.has_blocks:
            self.extract_blocks()

        if self.has_pdf and not self.has_worksheets:
            self.extract_worksheets()

        if self.has_blocks and not self.has_text:
            self.extract_text()
