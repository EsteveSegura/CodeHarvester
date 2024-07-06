import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.main import main

class TestMain(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.file_manipulation.file_operations.find_files_without_extensions')
    @patch('src.file_manipulation.file_operations.find_files')
    @patch('src.file_manipulation.tree_generator.print_tree')
    @patch('src.file_manipulation.tree_generator.print_tree_included')
    @patch('src.file_manipulation.file_operations.generate_markdown')
    @patch('src.gui.server.launch_server')
    @patch('src.utils.open_browser.open_url_in_browser')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_main_with_extensions(self, mock_isdir, mock_isfile, mock_listdir, mock_open_url, mock_launch_server, mock_generate_markdown, mock_print_tree_included, mock_print_tree, mock_find_files, mock_find_files_without_extensions, mock_open):
        mock_isdir.side_effect = lambda x: x.endswith('dir1') or x.endswith('dir2')
        mock_isfile.side_effect = lambda x: x.endswith('.py') or x.endswith('.js') or x.endswith('.txt')
        mock_listdir.side_effect = lambda x: {
            'dir': ['file1.py', 'file2.js', 'dir1'],
            'dir/dir1': ['file3.txt'],
            'dir/dir2': ['file4.txt']
        }.get(x, [])

        test_args = ["main.py", "dir", "--extensions", "py", "js"]
        with patch.object(sys, 'argv', test_args):
            main()

        mock_find_files.assert_called_once_with('dir', ['py', 'js'], [], [])
        mock_print_tree.assert_called_once_with('dir', exclude_dirs=[], exclude_files=[])

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.file_manipulation.file_operations.find_files_without_extensions')
    @patch('src.file_manipulation.file_operations.find_files')
    @patch('src.file_manipulation.tree_generator.print_tree')
    @patch('src.file_manipulation.tree_generator.print_tree_included')
    @patch('src.file_manipulation.file_operations.generate_markdown')
    @patch('src.gui.server.launch_server')
    @patch('src.utils.open_browser.open_url_in_browser')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_main_without_extensions(self, mock_isdir, mock_isfile, mock_listdir, mock_open_url, mock_launch_server, mock_generate_markdown, mock_print_tree_included, mock_print_tree, mock_find_files, mock_find_files_without_extensions, mock_open):
        mock_isdir.side_effect = lambda x: x.endswith('dir1') or x.endswith('dir2')
        mock_isfile.side_effect = lambda x: x.endswith('.py') or x.endswith('.js') or x.endswith('.txt')
        mock_listdir.side_effect = lambda x: {
            'dir': ['file1.py', 'file2.js', 'dir1'],
            'dir/dir1': ['file3.txt'],
            'dir/dir2': ['file4.txt']
        }.get(x, [])

        test_args = ["main.py", "dir"]
        with patch.object(sys, 'argv', test_args):
            main()

        mock_find_files_without_extensions.assert_called_once_with('dir', [], [])
        mock_print_tree.assert_called_once_with('dir', exclude_dirs=[], exclude_files=[])

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.file_manipulation.file_operations.find_files_without_extensions')
    @patch('src.file_manipulation.file_operations.find_files')
    @patch('src.file_manipulation.tree_generator.print_tree')
    @patch('src.file_manipulation.tree_generator.print_tree_included')
    @patch('src.file_manipulation.file_operations.generate_markdown')
    @patch('src.gui.server.launch_server')
    @patch('src.utils.open_browser.open_url_in_browser')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_main_output_to_file(self, mock_isdir, mock_isfile, mock_listdir, mock_open_url, mock_launch_server, mock_generate_markdown, mock_print_tree_included, mock_print_tree, mock_find_files, mock_find_files_without_extensions, mock_open):
        mock_isdir.side_effect = lambda x: x.endswith('dir1') or x.endswith('dir2')
        mock_isfile.side_effect = lambda x: x.endswith('.py') or x.endswith('.js') or x.endswith('.txt')
        mock_listdir.side_effect = lambda x: {
            'dir': ['file1.py', 'file2.js', 'dir1'],
            'dir/dir1': ['file3.txt'],
            'dir/dir2': ['file4.txt']
        }.get(x, [])

        test_args = ["main.py", "dir", "--output", "output.md"]
        with patch.object(sys, 'argv', test_args):
            main()

        mock_open.assert_called_once_with('output.md', 'w')
        mock_print_tree.assert_called_once_with('dir', exclude_dirs=[], exclude_files=[])

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.file_manipulation.file_operations.find_files_without_extensions')
    @patch('src.file_manipulation.file_operations.find_files')
    @patch('src.file_manipulation.tree_generator.print_tree')
    @patch('src.file_manipulation.tree_generator.print_tree_included')
    @patch('src.file_manipulation.file_operations.generate_markdown')
    @patch('src.gui.server.launch_server')
    @patch('src.utils.open_browser.open_url_in_browser', side_effect=MagicMock())
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_main_with_gui(self, mock_isdir, mock_isfile, mock_listdir, mock_open_url, mock_launch_server, mock_generate_markdown, mock_print_tree_included, mock_print_tree, mock_find_files, mock_find_files_without_extensions, mock_open):
        mock_isdir.side_effect = lambda x: x.endswith('dir1') or x.endswith('dir2')
        mock_isfile.side_effect = lambda x: x.endswith('.py') or x.endswith('.js') or x.endswith('.txt')
        mock_listdir.side_effect = lambda x: {
            'dir': ['file1.py', 'file2.js', 'dir1'],
            'dir/dir1': ['file3.txt'],
            'dir/dir2': ['file4.txt']
        }.get(x, [])

        test_args = ["main.py", "dir", "--gui"]
        with patch.object(sys, 'argv', test_args):
            main()

        #mock_open_url.assert_called_once_with('http://localhost:5043')
        mock_launch_server.assert_called_once()
        mock_print_tree.assert_called_once_with('dir', exclude_dirs=[], exclude_files=[])

if __name__ == '__main__':
    unittest.main()
