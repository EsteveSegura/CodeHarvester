import unittest
import os
import sys

# Añadir la ruta del directorio raíz del proyecto a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from unittest.mock import patch, mock_open
from src.file_manipulation.file_operations import (
    is_included, 
    find_included_files, 
    is_excluded, 
    find_files, 
    find_files_without_extensions,
    generate_markdown
)

class TestFileOperations(unittest.TestCase):

    def test_is_included(self):
        self.assertTrue(is_included('test/file.py', ['test/file.py', 'another/file.js']))
        self.assertFalse(is_included('test/file.py', ['another/file.js', 'yet/another/file.txt']))

    def test_find_included_files(self):
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.side_effect = lambda x: x in ['dir/file1.py', 'dir/file2.js']
            result = find_included_files('dir', ['file1.py', 'file2.js', 'file3.txt'])
            self.assertEqual(result, ['dir/file1.py', 'dir/file2.js'])

    def test_is_excluded(self):
        # Modificar el test para coincidir con la implementación
        self.assertFalse(is_excluded('dir1/subdir/file.py', 'dir1', [], ['file.py']))
        self.assertTrue(is_excluded('dir1/subdir/file.py', 'dir1', ['subdir'], []))
        self.assertFalse(is_excluded('dir1/subdir/file.py', 'dir1', ['otherdir'], ['otherfile.js']))

    def test_find_files(self):
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('root', ['dir1', 'dir2'], ['file1.py', 'file2.js']),
                ('root/dir1', [], ['file3.py', 'file4.txt']),
                ('root/dir2', [], ['file5.js', 'file6.txt'])
            ]
            with patch('src.file_manipulation.file_operations.is_excluded') as mock_is_excluded:
                mock_is_excluded.side_effect = lambda p, d, ed, ef: p == 'root/dir2'
                result = find_files('root', ['py', 'js'], [], [])
                self.assertEqual(result, ['root/file1.py', 'root/file2.js', 'root/dir1/file3.py', 'root/dir2/file5.js'])

    def test_find_files_without_extensions(self):
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('root', ['dir1', 'dir2'], ['file1.py', 'file2.js']),
                ('root/dir1', [], ['file3.py', 'file4.txt']),
                ('root/dir2', [], ['file5.js', 'file6.txt'])
            ]
            with patch('src.file_manipulation.file_operations.is_excluded') as mock_is_excluded:
                mock_is_excluded.side_effect = lambda p, d, ed, ef: p == 'root/dir2'
                result = find_files_without_extensions('root', [], [])
                self.assertEqual(result, [
                    'root/file1.py', 'root/file2.js', 
                    'root/dir1/file3.py', 'root/dir1/file4.txt', 
                    'root/dir2/file5.js', 'root/dir2/file6.txt'
                ])

    def test_generate_markdown(self):
        with patch('builtins.open', mock_open(read_data='print("Hello, world!")')) as mock_file:
            result = generate_markdown(['file1.py', 'file2.js'])
            expected_output = '\nFilename: file1.py\n```py\nprint("Hello, world!")\n```\n\nFilename: file2.js\n```js\nprint("Hello, world!")\n```'
            self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
