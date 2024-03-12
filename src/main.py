import os
import time
import fnmatch
import argparse

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
    parser.add_argument('--output', type=str, help='Output file path and name.', default=f"code_{int(time.time())}.md")

    args = parser.parse_args()

    exclude_dirs = [os.path.relpath(os.path.join(args.directory, e), args.directory) for e in args.exclude_dirs]
    exclude_files = [os.path.relpath(os.path.join(args.directory, e), args.directory) for e in args.exclude_files]

    files = find_files(args.directory, args.extensions, exclude_dirs, exclude_files)
    markdown = generate_markdown(files)
    tree = print_tree(args.directory, exclude_dirs=exclude_dirs, exclude_files=exclude_files)

    output_content = markdown + '\n\n' + tree

    print(output_content)

    with open(args.output, 'w') as file:
        file.write(output_content)

if __name__ == "__main__":
    main()
