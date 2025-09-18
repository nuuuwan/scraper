import os
from functools import cached_property

from utils import File, Log

log = Log("AbstractDocExtendedDataMixin")


class AbstractDocExtendedDataMixin:
    T_TIMEOUT_PDF_DOWNLOAD = 120

    @classmethod
    def get_remote_repo_url(cls) -> str:
        assert os.environ["GITHUB_USERNAME"]
        return "/".join(
            [
                "https://github.com",
                os.environ["GITHUB_USERNAME"],
                cls.get_doc_class_label(),
            ]
        )

    @classmethod
    def get_remote_data_url_base(cls) -> str:
        assert os.environ["GITHUB_USERNAME"]
        return "/".join(
            [
                cls.get_remote_repo_url(),
                "tree",
                "data",
            ]
        )

    @cached_property
    def remote_data_url(self) -> str:
        return "/".join(
            [
                self.get_remote_data_url_base(),
                self.__class__.get_dir_docs_for_cls_relative(),
                self.dir_doc_relative_to_class,
            ]
        )

    @classmethod
    def get_total_file_size(cls):
        total_size = 0
        for dirpath, _, filenames in os.walk(cls.get_dir_data_root()):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @cached_property
    def doc_readme_path(self) -> str:
        return os.path.join(self.dir_doc, "README.md")

    def get_text(self):
        if not os.path.exists(self.doc_readme_path):
            return ""
        return File(self.doc_readme_path).read()

    def scrape_extended_data_for_doc(self):
        raise NotImplementedError
