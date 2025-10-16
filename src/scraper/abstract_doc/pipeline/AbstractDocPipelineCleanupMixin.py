import os
import shutil

from utils import Log

log = Log("AbstractDocPipelineCleanupMixin")


class AbstractDocPipelineCleanupMixin:

    @classmethod
    def cleanup_doc_old_tabular_dirs(cls, doc):
        for dir_name in ["tabular", "worksheets"]:
            dir_path = os.path.join(doc.dir_doc, dir_name)
            if os.path.exists(dir_path):
                log.info(f"❌ Removing old dir: {dir_path}")
                shutil.rmtree(dir_path)

    @classmethod
    def cleanup_doc(cls, doc):
        cls.cleanup_doc_old_tabular_dirs(doc)

    @classmethod
    def cleanup_all(cls):
        docs = cls.list_all()
        for doc in docs:
            cls.cleanup_doc(doc)
