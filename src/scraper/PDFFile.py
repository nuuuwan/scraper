import os

import camelot
from utils import Directory, File, Log

log = Log('PDFFile')


class PDFFile(File):
    @property
    def dir_tables(self):
        return Directory(f'{self.path}.tables')

    @property
    def tables(self):
        path_list = []
        if self.dir_tables.exists:
            for file in self.dir_tables.children:
                if file.path.endswith('.tsv'):
                    path_list.append(file.path)
            return path_list

        os.mkdir(self.dir_tables.path)
        tables = camelot.read_pdf(self.path)
        for i, table in enumerate(tables):
            tsv_file_path = os.path.join(
                self.dir_tables.path, f'table-{i:02d}.tsv'
            )
            table.to_csv(tsv_file_path, sep='\t')
            path_list.append(tsv_file_path)
            log.debug(f'Saved {tsv_file_path}')

        return path_list
