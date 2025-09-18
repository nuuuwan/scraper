import os
import unittest
from unittest.mock import patch

import requests

from utils_future import WWW

TEST_WWW = WWW("https://mock.com")


class TestCase(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(TEST_WWW), "🌐 https://mock.com")

    def test_success(self):
        class MockResponse:
            def __init__(self):
                self.text = "<html><body>Hello</body></html>"
                self.status_code = 200

            def raise_for_status(self):
                pass

        mock_response = MockResponse()

        with patch.object(
            requests.Session,
            "get",
            return_value=mock_response,
        ):
            www = TEST_WWW
            self.assertEqual(www.content, "<html><body>Hello</body></html>")

            soup = www.soup
            body = soup.find("body").text
            self.assertEqual(body, "Hello")

            local_path = os.path.join("tests", "output", "test_binary.binary")
            www.download_binary(local_path)

    def test_download_binary_with_real(self):
        for i_real, url_pdf in enumerate(
            [
                "https://www.police.lk/wp-content/uploads"
                + "/2025/09/Media-on-2025.09.18-at-0630-_compressed.pdf"
            ]
        ):
            www = WWW(url_pdf)
            pdf_path = os.path.join("tests", "output", f"www-{i_real}.pdf")
            www.download_binary(pdf_path)
            self.assertTrue(os.path.exists(pdf_path))
            pdf_size = os.path.getsize(pdf_path)
            self.assertGreater(pdf_size, 1_000)
