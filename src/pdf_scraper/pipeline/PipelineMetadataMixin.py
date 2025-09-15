import time

from utils import Log

log = Log("PipelineMetadataMixin")


class PipelineMetadataMixin:

    @staticmethod
    def __log_processed_doc__(docs, dt):
        n_docs = len(docs)
        log.info(f"🛑 Processed {n_docs:,} docs in {dt:,.1f}s")

    def __scrape_metadata__(self, max_dt):
        t_start = time.time()
        home_page = self.home_page_class()
        docs = []
        dt = 0
        url_metadata_set = self.doc_class.get_url_metadata_set()
        for data_page in home_page.gen_data_pages():
            if data_page.url in url_metadata_set:
                continue
            for doc in data_page.gen_docs():
                doc.write()
                docs.append(doc)
            url_metadata_set.add(data_page.url)
            dt = time.time() - t_start
            if dt > max_dt:
                PipelineMetadataMixin.__log_processed_doc__(docs, dt)
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        PipelineMetadataMixin.__log_processed_doc__(docs, dt)
        log.info("🛑 All docs processed.")
