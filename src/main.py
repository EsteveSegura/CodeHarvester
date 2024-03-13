import os
import fnmatch
import argparse
import json
import time

def is_included(path, include_files):
    for include_file in include_files:
        if fnmatch.fnmatch(path, include_file):
            return True
    return False

def find_included_files(directory, include_files):
    matches = []
    for include_file in include_files:
        full_path = os.path.join(directory, include_file)
        if os.path.isfile(full_path):
            matches.append(full_path)
    return matches

def build_tree_from_included_files(directory, include_files):
    tree = {}

    for include_file in include_files:
        parts = include_file.split(os.sep)
        current_level = tree

        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    return tree

def print_tree_from_structure(structure, prefix=''):
    lines = []
    items = list(structure.items())
    for index, (name, subtree) in enumerate(items):
        connector = '└── ' if index == len(items) - 1 else '├── '
        lines.append(prefix + connector + name)
        if subtree:
            extension = '    ' if index == len(items) - 1 else '│   '
            lines.extend(print_tree_from_structure(subtree, prefix + extension))
    return lines

def print_tree_included(directory, include_files):
    tree_structure = build_tree_from_included_files(directory, include_files)
    return '\n'.join(print_tree_from_structure(tree_structure))

def is_excluded(path, directory, exclude_dirs, exclude_files):
    rel_path = os.path.relpath(path, directory)
    for exclude_dir in exclude_dirs:
        if rel_path.startswith(exclude_dir) or f"/{exclude_dir}/" in f"/{rel_path}/":
            return True
    for exclude_file in exclude_files:
        if fnmatch.fnmatch(rel_path, exclude_file):
            return True
    return False

def find_files(directory, extensions, exclude_dirs, exclude_files):
    matches = []
    for root, dirnames, filenames in os.walk(directory, topdown=True):
        dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(root, d), directory, exclude_dirs, exclude_files)]
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if any(filename.endswith(f'.{ext}') for ext in extensions) and not is_excluded(file_path, directory, exclude_dirs, exclude_files):
                matches.append(file_path)
    return matches

def print_tree(directory, prefix='', exclude_dirs=[], exclude_files=[]):
    tree_output = ""
    elements = os.listdir(directory)
    elements.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x.lower()))
    filtered_elements = [e for e in elements if not is_excluded(os.path.join(directory, e), directory, exclude_dirs, exclude_files)]

    for index, element in enumerate(filtered_elements):
        full_path = os.path.join(directory, element)
        is_last = index == len(filtered_elements) - 1
        prefix_element = '└── ' if is_last else '├── '
        tree_output += prefix + prefix_element + element + '\n'

        if os.path.isdir(full_path):
            secondary_prefix = '    ' if is_last else '│   '
            tree_output += print_tree(full_path, prefix + secondary_prefix, exclude_dirs, exclude_files)

    return tree_output

def build_tree_structure(directory, exclude_dirs=[], exclude_files=[]):
    tree = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path) and not is_excluded(full_path, directory, exclude_dirs, exclude_files):
            tree.append({
                "type": "folder",
                "name": item,
                "children": build_tree_structure(full_path, exclude_dirs, exclude_files)
            })
        elif os.path.isfile(full_path) and not is_excluded(full_path, directory, exclude_dirs, exclude_files):
            tree.append({
                "type": "file",
                "name": item
            })
    return tree

def generate_markdown(files):
    markdown_blocks = []
    for file in files:
        extension = file.split('.')[-1]
        with open(file, 'r') as f:
            content = f.read()
            markdown_blocks.append(f'\nFilename: {file}\n```{extension}\n{content}\n```')
    return '\n'.join(markdown_blocks)

def main():
    parser = argparse.ArgumentParser(description='Generate Markdown code blocks from code files in a directory structure.')
    parser.add_argument('directory', type=str, help='Root directory to start traversal.')
    parser.add_argument('--extensions', type=str, nargs='+', help='File extensions to include.', required=True)
    parser.add_argument('--exclude-dirs', type=str, nargs='*', default=[], help='Directories to exclude.')
    parser.add_argument('--exclude-files', type=str, nargs='*', default=[], help='Files to exclude.')
    parser.add_argument('--include-files', type=str, nargs='*', default=[], help='Specific files to include.')
    parser.add_argument('--output', type=str, help='Output file path and name.', default=f"code_{int(time.time())}.md")

    args = parser.parse_args()

    if args.include_files and (args.exclude_dirs or args.exclude_files):
        print("Error: --include-files cannot be used with --exclude-dirs or --exclude-files")
        return

    if args.include_files:
        include_files = [os.path.relpath(os.path.join(args.directory, f), args.directory) for f in args.include_files]
        files = find_included_files(args.directory, include_files)
        tree_text = print_tree_included(args.directory, include_files)
    else:
        exclude_dirs = [os.path.relpath(os.path.join(args.directory, e), args.directory) for e in args.exclude_dirs]
        exclude_files = [os.path.relpath(os.path.join(args.directory, e), args.directory) for e in args.exclude_files]
        files = find_files(args.directory, args.extensions, exclude_dirs, exclude_files) if args.extensions else []
        tree_text = print_tree(args.directory, exclude_dirs=exclude_dirs, exclude_files=exclude_files)
        # print(build_tree_structure(args.directory, exclude_dirs, exclude_files))

    markdown = generate_markdown(files)

    output_content = markdown + '\n\n' + tree_text

    print(output_content)

    with open(args.output, 'w') as file:
        file.write(output_content)

if __name__ == "__main__":
    main()
