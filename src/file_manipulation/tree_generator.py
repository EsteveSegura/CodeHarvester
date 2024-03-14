import os

def is_excluded(path, directory, exclude_dirs, exclude_files):
    rel_path = os.path.relpath(path, directory)
    for exclude_dir in exclude_dirs:
        if rel_path.startswith(exclude_dir) or f"/{exclude_dir}/" in f"/{rel_path}/":
            return True
    for exclude_file in exclude_files:
        if fnmatch.fnmatch(rel_path, exclude_file):
            return True
    return False

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