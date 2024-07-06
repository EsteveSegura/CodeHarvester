import unittest
import os
import sys
import fnmatch

# Añadir la ruta del directorio raíz del proyecto a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from unittest.mock import patch, mock_open
from src.file_manipulation.tree_generator import (
    is_excluded,
    build_tree_from_included_files,
    print_tree_from_structure,
    print_tree_included,
    print_tree,
    build_tree_structure
)

class TestTreeGenerator(unittest.TestCase):

    def test_is_excluded(self):
        self.assertTrue(is_excluded('dir1/subdir/file.py', 'dir1', [], ['subdir/file.py']))  
        self.assertFalse(is_excluded('dir1/subdir/file.py', 'dir1', [], ['otherfile.py']))

    def test_build_tree_from_included_files(self):
        include_files = ['dir1/file1.py', 'dir1/dir2/file2.js']
        expected_output = {
            'dir1': {
                'file1.py': {},
                'dir2': {
                    'file2.js': {}
                }
            }
        }
        result = build_tree_from_included_files('root', include_files)
        self.assertEqual(result, expected_output)

    def test_print_tree_from_structure(self):
        structure = {
            'dir1': {
                'file1.py': {},
                'dir2': {
                    'file2.js': {}
                }
            }
        }
        expected_output_lines = [
            '└── dir1',
            '    ├── file1.py',
            '    └── dir2',
            '        └── file2.js'
        ]
        result = print_tree_from_structure(structure)
        for line in expected_output_lines:
            self.assertIn(line, result)

    def test_print_tree_included(self):
        include_files = ['dir1/file1.py', 'dir1/dir2/file2.js']
        expected_output_lines = [
            '└── dir1',
            '    ├── file1.py',
            '    └── dir2',
            '        └── file2.js'
        ]
        result = print_tree_included('root', include_files)
        for line in expected_output_lines:
            self.assertIn(line, result.split('\n'))

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_print_tree(self, mock_isdir, mock_listdir):
        mock_listdir.side_effect = [
            ['dir1', 'file1.py', 'dir2'],
            ['file2.js'],
            ['file3.txt']
        ]
        mock_isdir.side_effect = lambda x: x in ['root/dir1', 'root/dir2']
        expected_output_lines = [
            '├── dir1',
            '│   └── file2.js',
            '├── dir2',
            '│   └── file3.txt',
            '└── file1.py'
        ]
        result = print_tree('root')
        for line in expected_output_lines:
            self.assertIn(line, result.split('\n'))

    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_build_tree_structure(self, mock_isfile, mock_isdir, mock_listdir):
        mock_listdir.side_effect = [
            ['dir1', 'file1.py', 'dir2'],
            ['file2.js'],
            ['file3.txt']
        ]
        mock_isdir.side_effect = lambda x: x in ['root/dir1', 'root/dir2']
        mock_isfile.side_effect = lambda x: x in ['root/file1.py', 'root/dir1/file2.js', 'root/dir2/file3.txt']
        expected_output = [
            {'type': 'folder', 'name': 'dir1', 'children': [{'type': 'file', 'name': 'file2.js'}]},
            {'type': 'file', 'name': 'file1.py'},
            {'type': 'folder', 'name': 'dir2', 'children': [{'type': 'file', 'name': 'file3.txt'}]}
        ]
        result = build_tree_structure('root')
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
