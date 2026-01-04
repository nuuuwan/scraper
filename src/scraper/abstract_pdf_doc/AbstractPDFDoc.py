import os
import shutil
import tempfile
from dataclasses import dataclass
from functools import cached_property

import camelot
from utils import WWW, File, JSONFile, Log, PDFFile

from scraper.abstract_doc import AbstractDoc
from scraper.abstract_doc.data_mixins.AbstractTabularMixin import (
    AbstractTabularMixin,
)

log = Log("AbstractPDFDoc")


@dataclass
class AbstractPDFDoc(AbstractTabularMixin, AbstractDoc):
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

            try:
                WWW(self.url_pdf).download_binary(temp_pdf_path)
            except Exception as e:
                log.error(f"Failed to download PDF from {self.url_pdf}: {e}")
                return

            try:
                PDFFile(temp_pdf_path).compress(self.pdf_path)
            except Exception as e:
                log.warning(f"Failed to compress PDF from {self.url_pdf}: {e}")
                shutil.move(temp_pdf_path, self.pdf_path)

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
        try:
            blocks = pdf_file.get_blocks()
            JSONFile(self.blocks_path).write(blocks)
            log.info(f"Wrote {self.blocks_path} ({len(blocks):,} blocks)")
        except Exception as e:
            log.error(f"Failed to extract blocks from {self.pdf_path}: {e}")
            return

    def get_blocks(self):
        return JSONFile(self.blocks_path).read()

    # ----------------------------------------------------------------
    # Worksheets (extracted from PDF)
    # ----------------------------------------------------------------

    @staticmethod
    def get_tables(pdf_path: str) -> camelot.core.TableList | None:

        try:
            os.environ["OMP_NUM_THREADS"] = "1"
            os.environ["OPENBLAS_NUM_THREADS"] = "1"
            os.environ["MKL_NUM_THREADS"] = "1"
            os.environ["NUMEXPR_NUM_THREADS"] = "1"

            tables = camelot.read_pdf(
                pdf_path,
                flavor="lattice",
                pages="all",
                process_background=False,
                line_scale=60,
            )
            n_tables = len(tables)
            log.debug(f"Found {n_tables} tables in {pdf_path}")
            return tables
        except Exception as e:
            log.error(f"Failed to extract tables from {pdf_path}: {e}")
            return None

    def extract_tabular(self):
        if not self.has_pdf:
            return

        tables = self.get_tables(self.pdf_path)
        if not tables or len(tables) == 0:
            log.info(f"No tables found in {self.pdf_path}")
            return

        os.makedirs(self.dir_tabular, exist_ok=True)
        tables.export(os.path.join(self.dir_tabular, "table.csv"), f="csv")

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
        lines = []
        for text, label in [
            (self.get_text_from_block(), "BLOCKS"),
            (self.get_text_from_tabular(), "WORKSHEETS"),
        ]:
            if text:
                lines.append(f"==== {label} ==== ")
                lines.append("")
                lines.append(text)
                lines.append("")

        return "\n".join(lines).strip()

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

        # if self.has_pdf and not self.has_tabular:
        #     self.extract_tabular()

        if self.has_blocks and not self.has_text:
            self.extract_text()
