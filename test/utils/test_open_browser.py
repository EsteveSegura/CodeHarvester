import unittest
from unittest.mock import patch, call
import sys
import subprocess
from src.utils.open_browser import open_url_in_browser

class TestOpenBrowser(unittest.TestCase):

    @patch('subprocess.run')
    @patch('sys.platform', 'linux')
    def test_open_url_in_browser_linux(self, mock_run):
        url = 'http://example.com'
        result = open_url_in_browser(url)
        mock_run.assert_called_once_with(['xdg-open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        self.assertTrue(result)

    @patch('subprocess.run')
    @patch('sys.platform', 'darwin')
    def test_open_url_in_browser_darwin(self, mock_run):
        url = 'http://example.com'
        result = open_url_in_browser(url)
        mock_run.assert_called_once_with(['open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        self.assertTrue(result)

    @patch('subprocess.run')
    @patch('sys.platform', 'win32')
    def test_open_url_in_browser_windows(self, mock_run):
        url = 'http://example.com'
        result = open_url_in_browser(url)
        mock_run.assert_called_once_with(['start', url], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        self.assertTrue(result)

    @patch('subprocess.run')
    @patch('sys.platform', 'unknown_platform')
    def test_open_url_in_browser_unsupported(self, mock_run):
        url = 'http://example.com'
        result = open_url_in_browser(url)
        mock_run.assert_not_called()
        self.assertFalse(result)

    @patch('subprocess.run', side_effect=Exception('Test Exception'))
    @patch('sys.platform', 'linux')
    def test_open_url_in_browser_exception(self, mock_run):
        url = 'http://example.com'
        result = open_url_in_browser(url)
        mock_run.assert_called_once_with(['xdg-open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
