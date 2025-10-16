import os

from utils import FileOrDirectory, JSONFile, Log, Time, TimeFormat

log = Log("AbstractDocSummaryMixin")


class AbstractDocSummaryMixin:

    @property
    def has_pdf(self) -> bool:
        return False

    @property
    def has_excel(self) -> bool:
        return False

    @property
    def has_tabular(self) -> bool:
        return False

    @staticmethod
    def get_url_source_list(doc_list) -> list:
        url_metadata_list = [doc.url_metadata for doc in doc_list]
        top_url_list = [
            "/".join(url.split("/")[:3]) for url in url_metadata_list
        ]
        top_url_to_n = {}
        for top_url in top_url_list:
            if top_url not in top_url_to_n:
                top_url_to_n[top_url] = 0
            top_url_to_n[top_url] += 1

        sorted_top_url_to_n = dict(
            sorted(
                top_url_to_n.items(), key=lambda item: item[1], reverse=True
            )
        )
        return list(sorted_top_url_to_n.keys())

    @classmethod
    def get_summary(cls) -> dict:
        doc_list = cls.list_all()  # used multiple times
        time_unit = cls.get_best_time_unit()  # reused below

        cls.build_chart_by_time_and_lang(
            cls.get_ts_to_lang_to_n(time_unit), time_unit
        )

        return dict(
            doc_class_label=cls.get_doc_class_label(),
            doc_class_emoji=cls.get_doc_class_emoji(),
            doc_class_description=cls.get_doc_class_description(),
            time_updated=TimeFormat.TIME.format(Time.now()),
            n_docs=len(doc_list),
            n_docs_with_pdfs=len([doc for doc in doc_list if doc.has_pdf]),
            n_docs_with_text=len([doc for doc in doc_list if doc.has_text]),
            n_docs_with_excel=len([doc for doc in doc_list if doc.has_excel]),
            n_docs_with_tabular=len(
                [doc for doc in doc_list if doc.has_tabular]
            ),
            date_str_min=min(doc.date_str for doc in doc_list),
            date_str_max=max(doc.date_str for doc in doc_list),
            dataset_size=FileOrDirectory(cls.get_data_branch_dir_root()).size,
            url_source_list=cls.get_url_source_list(doc_list),
            url_data=cls.get_remote_data_url_for_class(),
            url_chart=cls.get_raw_remote_chart_image_url(time_unit),
            langs=list({doc.lang for doc in doc_list}),
            latest_doc_d=doc_list[0].to_dict(),
        )

    @classmethod
    def get_summary_path(cls) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/summary.json
        return os.path.join(cls.get_dir_docs_for_cls(), "summary.json")

    @classmethod
    def build_summary(cls):
        summary = cls.get_summary()
        log.debug(f"{summary=}")
        summary_json_path = cls.get_summary_path()
        os.makedirs(cls.get_main_branch_dir_root(), exist_ok=True)
        JSONFile(summary_json_path).write(summary)
        log.info(f"Wrote {summary_json_path}")
