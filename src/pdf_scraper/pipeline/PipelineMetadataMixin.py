import time

from utils import Log

log = Log("PipelineMetadataMixin")


class PipelineMetadataMixin:

    @staticmethod
    def __log_processed_doc__(docs, dt):
        n_docs = len(docs)
        log.info(f"🛑 Processed {n_docs:,} docs in {dt:,.1f}s")

    def scrape_metadata(self, max_dt):
        t_start = time.time()
        docs = []
        dt = 0
        data_page = self.data_page_class()
        for doc in data_page.gen_docs():
            doc.write()
            docs.append(doc)
            dt = time.time() - t_start
            if dt > max_dt:
                PipelineMetadataMixin.__log_processed_doc__(docs, dt)
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        PipelineMetadataMixin.__log_processed_doc__(docs, dt)
        log.info("🛑 All docs processed.")
