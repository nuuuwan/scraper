import unittest

from utils_future import Chunker


class TestCase(unittest.TestCase):
    def test_chunk(self):
        chunk = "12345678\n\n" * 1_000
        max_chunk_size = 40
        min_overlap_size = 8
        chunks = Chunker.chunk(
            content=chunk,
            max_chunk_size=max_chunk_size,
            min_overlap_size=min_overlap_size,
        )
        self.assertEqual(len(chunks), 250)
        self.assertEqual(chunks[0], "12345678\n\n" * 3 + "12345678")
