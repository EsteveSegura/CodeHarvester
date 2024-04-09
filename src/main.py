import os
import fnmatch
import argparse
import json
import time

import file_manipulation.file_operations as fo
import file_manipulation.tree_generator as tg

import gui.server as server

def main():
    parser = argparse.ArgumentParser(description='Generate Markdown code blocks from code files in a directory structure.')
    parser.add_argument('directory', type=str, help='Root directory to start traversal.')
    parser.add_argument('--extensions', type=str, nargs='+', help='File extensions to include.', required=False)
    parser.add_argument('--exclude-dirs', type=str, nargs='*', default=[], help='Directories to exclude.')
    parser.add_argument('--exclude-files', type=str, nargs='*', default=[], help='Files to exclude.')
    parser.add_argument('--include-files', type=str, nargs='*', default=[], help='Specific files to include.')
    parser.add_argument('--output', type=str, help='Output file path and name.', default='')
    parser.add_argument('--gui', type=bool, default=False, help='Launch a server to display the output file.')

    args = parser.parse_args()

    if args.include_files and (args.exclude_dirs or args.exclude_files):
        print("Error: --include-files cannot be used with --exclude-dirs or --exclude-files")
        return

    if args.include_files:
        include_files = [os.path.relpath(os.path.join(args.directory, f), args.directory) for f in args.include_files]
        files = fo.find_included_files(args.directory, include_files)
        tree_text = tg.print_tree_included(args.directory, include_files)
    else:
        exclude_dirs = [os.path.relpath(os.path.join(args.directory, e), args.directory) for e in args.exclude_dirs]
        exclude_files = [os.path.relpath(os.path.join(args.directory, e), args.directory) for e in args.exclude_files]
        if args.extensions:
            files = fo.find_files(args.directory, args.extensions, exclude_dirs, exclude_files)
        else:
            files = fo.find_files_without_extensions(args.directory, exclude_dirs, exclude_files)
        tree_text = tg.print_tree(args.directory, exclude_dirs=exclude_dirs, exclude_files=exclude_files)
        structure_file_json = tg.build_tree_structure(args.directory, exclude_dirs, exclude_files)
        if args.gui:
            server.launch_server(structure_file_json, args.directory)

    markdown = fo.generate_markdown(files)
    output_content = markdown + '\n\n' + tree_text

    if not args.gui:
        print(output_content)

    if args.output != '':
        with open(args.output, 'w') as file:
            file.write(output_content)

if __name__ == "__main__":
    main()
