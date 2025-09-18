import os
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import File, JSONFile, Log

from scraper.abstract_doc import AbstractDoc
from utils_future import WWW, PDFFile

log = Log("AbstractPDFDoc")


@dataclass
class AbstractPDFDoc(AbstractDoc, ABC):
    url_pdf: str

    @cached_property
    def pdf_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "doc.pdf")

    @property
    def has_pdf(self) -> bool:
        return os.path.exists(self.pdf_path)

    @cached_property
    def blocks_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "blocks.json")

    def extract_blocks(self):
        assert os.path.exists(self.pdf_path)
        pdf_file = PDFFile(self.pdf_path)
        blocks = pdf_file.get_blocks()
        JSONFile(self.blocks_path).write(blocks)
        log.info(f"Wrote {self.blocks_path} ({len(blocks):,} blocks)")

        text_lines = [block["text"] for block in blocks if block["text"]]
        File(self.doc_readme_path).write("\n\n".join(text_lines))
        log.info(f"Wrote {self.doc_readme_path}")

    def get_blocks(self):
        assert os.path.exists(self.blocks_path)
        return JSONFile(self.blocks_path).read()

    def scrape_extended_data_for_doc_text_part(self):
        if not self.has_pdf:
            WWW(self.url_pdf).download_binary(self.pdf_path)
        if not os.path.exists(self.blocks_path) or not os.path.getsize(
            self.doc_readme_path
        ):
            self.extract_blocks()
