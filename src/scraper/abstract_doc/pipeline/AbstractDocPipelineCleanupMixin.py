import os
import shutil

from utils import JSONFile, Log

log = Log("AbstractDocPipelineCleanupMixin")


class AbstractDocPipelineCleanupMixin:

    @classmethod
    def cleanup_incorrect_doc_dir(cls, json_path):
        doc = cls.from_file(json_path)
        dir_doc_actual = os.path.dirname(json_path)
        dir_doc_expected = doc.dir_doc.lstrip("./")
        if dir_doc_actual != dir_doc_expected:
            log.warning(
                f"doc_id={doc.doc_id} in wrong dir:"
                + f" {dir_doc_expected} != {dir_doc_actual}"
            )
            shutil.rmtree(dir_doc_actual)
            log.warning(f"🧹 Deleted {dir_doc_actual}")

    @classmethod
    def add_lang(cls, json_path):
        json_file = JSONFile(json_path)
        d = json_file.read()
        if "lang" not in d:
            d["lang"] = "en"
            json_file.write(d)
            log.warning(f"➕ Added lang=en to {json_path}")

    @classmethod
    def cleanup_all_by_file_path(cls):
        for json_path in cls.get_all_json_paths():
            cls.add_lang(json_path)
            cls.cleanup_incorrect_doc_dir(json_path)

    @classmethod
    def correct_pdf_path(cls, doc):
        expected_pdf_path = os.path.join(doc.dir_doc_extended, "doc.pdf")
        legacy_pdf_path = os.path.join(doc.dir_doc_extended, "en.pdf")

        if os.path.exists(legacy_pdf_path):
            if os.path.exists(expected_pdf_path):
                os.remove(legacy_pdf_path)
                log.warning(
                    f"🧹 Deleted legacy {legacy_pdf_path}"
                    + f" ({expected_pdf_path} exists)"
                )
            else:
                shutil.move(legacy_pdf_path, expected_pdf_path)
                log.warning(
                    f"🔄 Moved {legacy_pdf_path} to {expected_pdf_path}"
                )

    @classmethod
    def cleanup_all_by_doc(cls):
        for doc in cls.list_all():
            cls.correct_pdf_path(doc)

    @classmethod
    def cleanup_all(cls):
        cls.cleanup_all_by_file_path()
        cls.cleanup_all_by_doc()
