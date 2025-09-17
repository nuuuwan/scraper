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
