import os
import fnmatch

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

def find_files_without_extensions(directory, exclude_dirs, exclude_files):
    matches = []
    for root, dirnames, filenames in os.walk(directory, topdown=True):
        dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(root, d), directory, exclude_dirs, exclude_files)]
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not is_excluded(file_path, directory, exclude_dirs, exclude_files):
                matches.append(file_path)
    return matches

# ToDo: Add a verbose option to print out the files that are skipped in main.py
def generate_markdown(files, verbose=False):
    markdown_blocks = []
    for file in files:
        extension = file.split('.')[-1]
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                markdown_blocks.append(f'\nFilename: {file}\n```{extension}\n{content}\n```')
        except UnicodeDecodeError as e:
            if verbose:
                print(f"Error when reading {file}: its a binary file. Skipping.")
    return '\n'.join(markdown_blocks)