import os
from dataclasses import asdict
from functools import cached_property

import pandas as pd
from datasets import Dataset
from utils import Hash, Log

from pdf_scraper.abstract_doc import AbstractDoc
from utils_future import BigJSONFile, Chunker

log = Log("HuggingFaceDataset")


class HuggingFaceDataset:
    MAX_CHUNK_SIZE = 2000
    MIN_OVERLAP_SIZE = 200
    HUGGING_FACE_USERNAME = os.environ.get("HUGGING_FACE_USERNAME")
    HUGGING_FACE_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")

    def __init__(self, doc_class: AbstractDoc):
        self.doc_class = doc_class
        self.doc_list = self.doc_class.list_all()

    @cached_property
    def docs_json_path(self):
        return os.path.join(self.doc_class.get_dir_extended_root(), "docs")

    def build_docs(self):
        d_list = [asdict(doc) for doc in self.doc_list]
        BigJSONFile(self.docs_json_path).write(d_list)
        return d_list

    @staticmethod
    def get_data_list_for_doc(doc):
        chunks = Chunker.chunk(
            doc.get_text(),
            HuggingFaceDataset.MAX_CHUNK_SIZE,
            HuggingFaceDataset.MIN_OVERLAP_SIZE,
        )
        d_list = []
        for chunk_index, chunk_text in enumerate(chunks):
            chunk_id = f"{doc.doc_id}-{chunk_index:04d}"
            d = asdict(doc) | dict(
                chunk_id=chunk_id,
                chunk_index=chunk_index,
                language="en",
                md5=Hash.md5(chunk_text),
                chunk_size_bytes=len(chunk_text.encode("utf-8")),
                chunk_text=chunk_text,
            )
            d_list.append(d)

        return d_list

    @cached_property
    def chunks_json_path(self):
        return os.path.join(self.doc_class.get_dir_extended_root(), "chunks")

    def build_chunks(self):
        d_list = []
        for doc in self.doc_list:
            d_list.extend(HuggingFaceDataset.get_data_list_for_doc(doc))

        BigJSONFile(self.chunks_json_path).write(d_list)
        return d_list

    @cached_property
    def hugging_face_project(self):
        return "/".join(
            [
                self.HUGGING_FACE_USERNAME,
                f"lk-docs-{self.doc_class.doc_class_label()}",
            ]
        )

    def get_dataset_id(self, label_suffix: str) -> str:
        return f"{self.hugging_face_project}-{label_suffix}"

    def get_dataset_url(self, label_suffix: str) -> str:
        return (
            "https://huggingface.co/datasets"
            + f"/{self.get_dataset_id(label_suffix)}"
        )

    def upload_to_hugging_face(self):
        docs_df = pd.DataFrame(self.build_docs())
        chunks_df = pd.DataFrame(self.build_chunks())
        docs_ds = Dataset.from_pandas(docs_df)
        chunks_ds = Dataset.from_pandas(chunks_df)
        assert self.HUGGING_FACE_USERNAME
        assert self.HUGGING_FACE_TOKEN

        for ds, suffix in [(docs_ds, "docs"), (chunks_ds, "chunks")]:
            dataset_id = self.get_dataset_id(suffix)
            repo_id = ds.push_to_hub(
                dataset_id, token=self.HUGGING_FACE_TOKEN
            )
            log.info(f"🤗 Uploaded {dataset_id} to {repo_id}")

    def build_and_upload(self):
        if not self.doc_list:
            log.error(
                "No documents found. Not building Hugging Face dataset."
            )
            return
        self.upload_to_hugging_face()
