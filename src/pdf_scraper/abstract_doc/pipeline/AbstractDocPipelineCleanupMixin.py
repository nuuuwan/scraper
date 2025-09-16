import os
import shutil

from utils import Log

log = Log("AbstractDocPipelineCleanupMixin")


class AbstractDocPipelineCleanupMixin:
    @classmethod
    def cleanup_all(cls):
        delete_dir_docs = []
        for json_path in cls.get_all_json_paths():
            doc = cls.from_file(json_path)
            dir_doc_read = os.path.dirname(json_path)
            dir_doc_expected = doc.dir_doc.lstrip("./")
            if dir_doc_read != dir_doc_expected:
                log.warning(
                    f"doc_id={doc.doc_id} in wrong dir:"
                    + f" {dir_doc_expected} != {dir_doc_read}"
                )
                delete_dir_docs.append(dir_doc_read)

        n_delete = len(delete_dir_docs)
        log.warning(f"Deleting {n_delete} dirs")
        for dir_doc in delete_dir_docs:
            shutil.rmtree(dir_doc)
            log.warning(f"Deleted {dir_doc}")
