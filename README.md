# CodeHarvester

CodeHarvester is a command-line utility designed to collect and document source code from a project. It allows developers to easily generate an overview of their project structure and the content of selected files.

## Parameters

### Parameter Descriptions

- `-h, --help`: Display the help message with all available options.
- `-d, --directory <path>`: Specify the root directory to start the file search (required).
- `-e, --extensions <ext1> <ext2> ...`: Specify a list of file extensions to include.
- `-E, --exclude-extensions <ext1> <ext2> ...`: Specify file extensions to exclude.
- `-x, --exclude-dirs <dir1> <dir2> ...`: List of directories to exclude from the search.
- `-f, --exclude-files <file1> <file2> ...`: List of specific files to exclude.
- `--list-files <file1> <file2> ...`: List of specific files to process (relative to the root directory).
- `-o, --output <file>`: Path and name of the output file where the result will be saved (default: output.md).
- `--unlimited`: Process files of any size (by default, limited to 10MB).
- `--allow-binary-files`: Allow binary files to be processed and included in the output.
- `--diff`: If this option is specified, the Git diff of each file with changes will be included in the output. (Requires Git installed)

## Modes of Operation

### Normal Mode

In Normal Mode, CodeHarvester processes directories and subdirectories starting from the specified root directory. You can specify file extensions to include or exclude, as well as directories and files to exclude. This mode generates a Markdown document with the project structure and content of the found files.

#### Available options in Normal Mode:

- `-d, --directory <path>`: Specify the root directory to start the file search (required).
- `-e, --extensions <ext1> <ext2> ...`: Specify a list of file extensions to include.
- `-E, --exclude-extensions <ext1> <ext2> ...`: Specify file extensions to exclude.
- `-x, --exclude-dirs <dir1> <dir2> ...`: List of directories to exclude from the search.
- `-f, --exclude-files <file1> <file2> ...`: List of specific files to exclude.
- `-o, --output <file>`: Path and name of the output file where the result will be saved (default: output.md).
- `--unlimited`: Process files of any size (by default, limited to 10MB).
- `--allow-binary-files`: Allow binary files to be processed and included in the output.
- `--diff`: Include the Git diff of each file if changes are present.

### List Files Mode

In List Files Mode, CodeHarvester processes a specified list of files relative to the root directory. This mode is useful when you only want to document specific files instead of traversing entire directories.

#### Available options in List Files Mode:

- `-d, --directory <path>`: Specify the root directory to start the file search (required).
- `--list-files <file1> <file2> ...`: List of specific files to process (relative to the root directory).
- `-o, --output <file>`: Path and name of the output file where the result will be saved (default: output.md).
- `--unlimited`: Process files of any size (by default, limited to 10MB).
- `--allow-binary-files`: Allow binary files to be processed and included in the output.
- `--diff`: Include the Git diff of each file if changes are present.

## Output

CodeHarvester generates a Markdown file containing the structure and content of the specified files and directories. The output includes the following sections:

1. **Project Structure**: A tree representation of the project's directory structure.
2. **File Contents**: The content of the found files, formatted in code blocks.
3. **Git Diff (if `--diff` is used)**: The Git diff of each file with changes, formatted in diff code blocks.

### Example

Assuming you have the following directory structure:

```
/project
├── src
│   ├── main.cpp
│   └── util.cpp
├── include
│   └── util.h
└── CMakeLists.txt
```

And you run the following command:

```
./CodeHarvester -d /path/to/project -o output.md --extensions .cpp .h --diff
```

The generated `output.md` might look like this: [OUTPUT_EXAMPLE.md](OUTPUT_EXAMPLE.md)

In this example, the output file `output.md` includes the project structure, the content of `main.cpp`, `util.cpp`, and `util.h`, and the Git diff for `main.cpp` showing the changes made.

## Usage

The basic syntax for using CodeHarvester is:

```shell
./CodeHarvester [options]
```

### Usage examples

1. Process all files in a directory:
   ```shell
   ./CodeHarvester -d /path/to/your/project -o output.md
   ```

2. Include only files with specific extensions (.cpp & .h):
   ```shell
   ./CodeHarvester -d /path/to/your/project -e .cpp .h -o output.md
   ```

3. Exclude certain directories and files:
   ```shell
   ./CodeHarvester -d /path/to/your/project -x build .git -f .env -o output.md
   ```

4. Process only specific files:
   ```shell
   ./CodeHarvester -d /path/to/your/project --list-files src/main.cpp include/header.h -o output.md
   ```

5. Process files of any size and allow binary files:
   ```shell
   ./CodeHarvester -d /path/to/your/project --unlimited --allow-binary-files -o output.md
   ```

## Building the Project

### Prerequisites

- C++ compiler with C++17 support
- CMake (version 3.10 or higher)
- Boost library (program_options and filesystem components)

### Build

1. Clone the repository:
   ```bash
   git clone https://github.com/EsteveSegura/CodeHarvester.git
   cd CodeHarvester
   ```

2. Create a build directory and navigate to it:
   ```bash
   mkdir build && cd build
   ```

3. Run CMake and build the project:
   ```bash
   cmake ..
   make
   ```

## License

MIT
