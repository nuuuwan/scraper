import os
import shutil
from functools import cached_property

from utils import File, JSONFile, Log

from utils_future import WWW, PDFFile

log = Log("AbstractDocExtendedDataMixin")


class AbstractDocExtendedDataMixin:
    T_TIMEOUT_PDF_DOWNLOAD = 120

    @cached_property
    def dir_doc_extended_without_base(self) -> str:
        return os.path.join(
            "data",
            self.__class__.doc_class_label(),
            self.decade,
            self.year,
            self.doc_id,
        )

    @classmethod
    def get_dir_extended_root(cls) -> str:
        dir_metadata = os.path.basename(os.getcwd())
        return os.path.join(
            "..",
            f"{dir_metadata}_data",
        )

    @cached_property
    def dir_doc_extended(self) -> str:
        return os.path.join(
            self.__class__.get_dir_extended_root(),
            self.dir_doc_extended_without_base,
        )

    def copy_metadata(self):
        shutil.copytree(
            self.dir_doc, self.dir_doc_extended, dirs_exist_ok=True
        )
        log.info(f"Copied metadata to {self.dir_doc_extended}")

    @cached_property
    def pdf_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "en.pdf")

    @property
    def has_pdf(self) -> bool:
        return os.path.exists(self.pdf_path)

    @cached_property
    def remote_data_url(self) -> str:
        raise NotImplementedError

    @cached_property
    def blocks_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "blocks.json")

    @cached_property
    def readme_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "README.md")

    def extract_blocks(self):
        if not os.path.exists(self.pdf_path):
            return
        pdf_file = PDFFile(self.pdf_path)
        blocks = pdf_file.get_block_info_list()
        JSONFile(self.blocks_path).write(blocks)
        log.info(f"Wrote {len(blocks):,} blocks to {self.blocks_path}")

        text_lines = [block["text"] for block in blocks if block["text"]]
        File(self.readme_path).write("\n\n".join(text_lines))
        log.info(f"Wrote README.md to {self.readme_path}")

    def scrape_extended_data(self):
        if not os.path.exists(self.dir_doc_extended):
            os.makedirs(self.dir_doc_extended)
            self.copy_metadata()
        if not self.has_pdf:
            WWW(self.url_pdf).download_binary(self.pdf_path)
        if not os.path.exists(self.blocks_path):
            self.extract_blocks()

    def get_text(self):
        if not os.path.exists(self.readme_path):
            return ""
        return File(self.readme_path).read()

    @classmethod
    def get_total_file_size(cls):
        total_size = 0
        for dirpath, _, filenames in os.walk(cls.get_dir_extended_root()):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
