import os
from typing import Generator

from utils import File, JSONFile, Log

from scraper import AbstractDoc

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    @classmethod
    def get_summary_path_for_doc_class(cls, doc_class_label: str) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/summary.json
        return os.path.join(
            AbstractDoc.get_data_branch_dir_root_data(),
            doc_class_label,
            "summary.json",
        )

    @classmethod
    def get_summary_for_doc_class(cls, doc_class_label: str) -> dict:
        return JSONFile(
            cls.get_summary_path_for_doc_class(doc_class_label)
        ).read()

    @classmethod
    def get_lines_for_doc_class(cls, doc_class_label: str) -> list[str]:
        summary = cls.get_summary_for_doc_class(doc_class_label)
        return AbstractDoc.get_lines_for_header(
            summary
        ) + AbstractDoc.get_lines_for_blurb(summary)

    @classmethod
    def gen_doc_class_labels(cls) -> Generator[str, None, None]:
        root_path = AbstractDoc.get_data_branch_dir_root_data()
        for child_name in os.listdir(root_path):
            child_path = os.path.join(root_path, child_name)
            if os.path.isdir(child_path):
                yield child_name

    @classmethod
    def get_lines_for_doc_classes(cls) -> list[str]:
        lines = []
        for doc_class_label in cls.gen_doc_class_labels():
            lines.extend(cls.get_lines_for_doc_class(doc_class_label))
        return lines

    @classmethod
    def get_lines(cls) -> list[str]:
        return (
            cls.get_lines_for_doc_classes()
            + AbstractDoc.get_lines_for_footer()
        )

    @classmethod
    def build(cls):
        File(cls.PATH).write_lines(cls.get_lines())
        log.info(f"Wrote {cls.PATH}")
