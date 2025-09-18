import os

from utils import JSONFile, Log, Time, TimeFormat

from utils_future import FileOrDirFuture

log = Log("AbstractDocSummaryMixin")


class AbstractDocSummaryMixin:
    @classmethod
    def get_summary_path(cls) -> str:
        return os.path.join(cls.get_main_branch_dir_root(), "summary.json")

    @classmethod
    def get_summary(cls) -> dict:
        doc_class_label = cls.get_doc_class_label()
        time_updated = TimeFormat.TIME.format(Time.now())
        n_docs = len(cls.list_all())
        n_docs_with_pdfs = len([doc for doc in cls.list_all() if doc.has_pdf])
        n_docs_with_text = len(
            [doc for doc in cls.list_all() if doc.has_text]
        )
        date_strs = [doc.date_str for doc in cls.list_all()]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)
        dataset_size = FileOrDirFuture(cls.get_data_branch_dir_root()).size
        latest_doc = cls.list_all()[0]
        url_source = latest_doc.url_metadata.split("?")[0]
        url_data = cls.get_remote_data_url_base()
        url_repo = cls.get_remote_repo_url()
        latest_doc = cls.list_all()[0]
        latest_doc_d = latest_doc.to_dict()

        return dict(
            doc_class_label=doc_class_label,
            time_updated=time_updated,
            n_docs=n_docs,
            n_docs_with_pdfs=n_docs_with_pdfs,
            n_docs_with_text=n_docs_with_text,
            date_str_min=date_str_min,
            date_str_max=date_str_max,
            dataset_size=dataset_size,
            url_source=url_source,
            url_data=url_data,
            url_repo=url_repo,
            latest_doc_d=latest_doc_d,
        )

    @classmethod
    def build_summary(cls):
        summary = cls.get_summary()
        log.debug(f"{summary=}")
        summary_json_path = cls.get_summary_path()
        JSONFile(summary_json_path).write(summary)
        log.info(f"Wrote {summary_json_path}")
