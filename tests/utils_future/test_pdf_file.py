import os
import unittest

from utils_future import PDFFile


class TestCase(unittest.TestCase):
    def test_all(self):
        pdf_file = PDFFile(os.path.join("tests", "input", "test.pdf"))
        block_info_list = pdf_file.get_blocks()
        self.assertEqual(len(block_info_list), 6)

        en_block = block_info_list[3]
        self.assertEqual(
            en_block,
            {
                "page_number": 0,
                "bbox": (72.47, 181.87, 186.95, 195.07),
                "text": "Some text in English.",
                "fonts": ["Palatino-Roman"],
                "sizes": [12.0],
            },
        )

        si_block = block_info_list[4]
        self.assertEqual(
            si_block,
            {
                "page_number": 0,
                "bbox": (72.47, 205.72, 335.44, 230.98),
                "text": "!ංහෙල& 'ය)* ය+ පාඨය/.",
                "fonts": ["HelveticaNeue", "IskoolaPota"],
                "sizes": [21.119998931884766],
            },
        )

        ta_block = block_info_list[5]
        print(ta_block)
        self.assertEqual(
            ta_block,
            {
                "page_number": 0,
                "bbox": (72.47, 242.87, 216.68, 262.79),
                "text": "தமிழி% சில உைரக,.",
                "fonts": ["Latha", "Palatino-Roman"],
                "sizes": [12.0],
            },
        )

        image_path = os.path.join("tests", "output", "test_page1.png")
        pdf_file.download_image(0, image_path)
