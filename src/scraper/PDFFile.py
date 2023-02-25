import os

import camelot
from utils import Directory, File, Log

log = Log('PDFFile')


class PDFFile(File):
    @staticmethod
    def is_remote_url_pdf(url):
        return url.endswith('.pdf')

    @property
    def dir_tables(self):
        return Directory(f'{self.path}.tables')

    def load_tables_from_local(self):
        path_list = []
        print(os.system(f'ls -la {self.dir_tables.path}'))
        for file in self.dir_tables.children:
            if file.path.endswith('.tsv'):
                path_list.append(file.path)
        log.debug(
            f'Loaded {len(path_list)} table(s) from {self.dir_tables.path}'
        )
        return path_list

    def get_camelot_tables(self):
        try:
            return camelot.read_pdf(self.path)
        except BaseException:
            log.error(f'Failed to read {self.path}')
            return []

    def save_camelot_table(self, i, table):
        tsv_file_path = os.path.join(
            self.dir_tables.path, f'table-{i:02d}.tsv'
        )
        table.to_csv(tsv_file_path, sep='\t')
        log.debug(f'Saved {tsv_file_path}')
        return tsv_file_path

    def store_tables_to_local(self):
        os.mkdir(self.dir_tables.path)
        path_list = []
        for i, table in enumerate(self.get_camelot_tables()):
            path_list.append(self.save_camelot_table(i, table))
        log.debug(f'Stored {len(path_list)} table to {self.dir_tables.path}')
        return path_list

    @property
    def tables(self):
        if self.dir_tables.exists:
            return self.load_tables_from_local()
        return self.store_tables_to_local()
