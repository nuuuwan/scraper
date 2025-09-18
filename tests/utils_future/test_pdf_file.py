import os
import unittest

from utils_future import PDFFile


class TestCase(unittest.TestCase):
    def test_all(self):
        pdf_file = PDFFile(os.path.join("tests", "input", "test.pdf"))
        blocks = pdf_file.get_blocks()
        self.assertEqual(len(blocks), 6)
        en_block = blocks[3]
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

        si_block = blocks[4]
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

        ta_block = blocks[5]
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

    def test_si(self):
        pdf_file = PDFFile(os.path.join("tests", "input", "si.pdf"))
        blocks = pdf_file.get_blocks()
        self.assertEqual(len(blocks), 13)

        self.assertEqual(
            blocks[0],
            {
                "page_number": 0,
                "bbox": (72.02, 137.08, 400.69, 267.79),
                "text": "ප ොලිස් මොධ්\u200dය ප ොට්ඨොසය පෙත ෙොර්තො වූ ෙැදගත් පතොරතුරු 01. මනුෂ්\u200dය ඝොතනයක් - තිස්සමහොරොම ප ොලිස් ෙසම.",
                "fonts": ["IskoolaPota-Bold"],
                "sizes": [
                    6.960000038146973,
                    9.960000038146973,
                    14.039999961853027,
                ],
            },
        )

        self.assertEqual(
            blocks[7],
            {
                "page_number": 1,
                "bbox": (72.02, 36.38, 527.01, 77.3),
                "text": "03. දය අනතුරකින් තරුණයින් තිපදපනකු පේරො ගැනීම - ප ොලිස් ජීවිතොරක්ෂ්\u200d ඒ ය ගල්කකිස්ස.",
                "fonts": ["IskoolaPota-Bold"],
                "sizes": [6.960000038146973, 14.039999961853027],
            },
        )
