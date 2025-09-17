import os
import unittest

from utils_future import PDFFile


class TestCase(unittest.TestCase):
    def test_all(self):
        pdf_file = PDFFile(os.path.join("tests", "input", "test.pdf"))
        block_info_list = pdf_file.get_blocks()
        self.assertEqual(len(block_info_list), 4)
        first_block = block_info_list[0]
        self.assertEqual(
            first_block,
            {
                "page_number": 0,
                "bbox": (72.03, 90.13, 187.66, 121.07),
                "text": "Heading 1",
                "fonts": ["SegoeUIHistoric"],
                "sizes": [24.0],
            },
        )

        image_path = os.path.join("tests", "output", "test_page1.png")
        pdf_file.download_image(0, image_path)
