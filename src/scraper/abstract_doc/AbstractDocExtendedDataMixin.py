import os
import shutil
from functools import cached_property

from utils import File, Log

log = Log("AbstractDocExtendedDataMixin")


class AbstractDocExtendedDataMixin:
    T_TIMEOUT_PDF_DOWNLOAD = 120

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
            self.get_dir_docs_for_cls_relative(),
            self.dir_doc_relative_to_class,
        )

    def copy_metadata(self):
        shutil.copytree(
            self.dir_doc, self.dir_doc_extended, dirs_exist_ok=True
        )
        log.info(f"Copied metadata to {self.dir_doc_extended}")

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
        for dirpath, _, filenames in os.walk(cls.get_dir_extended_root()):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @cached_property
    def doc_readme_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "README.md")

    def get_text(self):
        if not os.path.exists(self.doc_readme_path):
            return ""
        return File(self.doc_readme_path).read()

    def scrape_extended_data_for_doc_text_part(self):
        raise NotImplementedError

    def scrape_extended_data_for_doc(self):
        if not os.path.exists(self.dir_doc_extended):
            os.makedirs(self.dir_doc_extended)
            self.copy_metadata()
        self.scrape_extended_data_for_doc_text_part()
