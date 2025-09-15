import os
import unittest
from unittest.mock import MagicMock, patch

from utils_future import WWW


class TestCase(unittest.TestCase):
    def test_str(self):
        www = WWW("https://mock.com")
        self.assertEqual(str(www), "🌐 https://mock.com")

    @patch("utils_future.WWW.requests.get")
    def test_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.text = "<html><body>Hello</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        www = WWW("https://mock.com")
        content = www.content
        self.assertEqual(content, "<html><body>Hello</body></html>")

        soup = www.soup
        body = soup.find("body").text
        self.assertEqual(body, "Hello")

        www = WWW("https://mock.com")
        local_path = os.path.join("tests", "output", "test_binary.binary")
        www.download_binary(local_path)

    @patch("utils_future.WWW.requests.get")
    def test_fail(self, mock_get):
        mock_get.side_effect = Exception("Connection failed")

        www = WWW("https://mock.com")
        self.assertIsNone(www.content)
        self.assertIsNone(www.soup)
