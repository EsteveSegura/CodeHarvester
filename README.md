# CodeHarvester

CodeHarvester efficiently aggregates code and text from files for streamlined AI analysis, simplifying data compilation for prompts.

![Demo of the GUI](./assets/demo.gif)

## Clone the Repository

To begin, clone the repository to your local machine:

```bash
git clone https://github.com/EsteveSegura/CodeHarvester.git
cd CodeHarvester
```

## Installation

Install the necessary dependencies to ensure CodeHarvester runs smoothly:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Command Line Usage

To use CodeHarvester from the command line, navigate to the CodeHarvester directory and execute the following command:

```bash
python3 src/main.py <ROOT_DIRECTORY> --extensions <FILE_EXTENSIONS> --exclude-dirs <DIRECTORIES_TO_EXCLUDE> --exclude-files <FILES_TO_EXCLUDE>
```

### Parameters

- `<ROOT_DIRECTORY>`: The starting point for the directory traversal.
- `--extensions`: Specify file extensions to include in the aggregation (e.g., py, js, txt).
- `--exclude-dirs`: List directories you wish to exclude from the traversal.
- `--exclude-files`: Specify individual files to be omitted from the aggregation.
- `--include-files`: Specify individual files to be aggregated (cannot be used with --exclude-dirs, --exclude-files).
- `--output`: Specify output file path and name. If not specified, the output will be printed to the console.
- `--gui`: Launch a server to display the output in a web interface. Use `True` to enable this mode.

### Running in GUI Mode

To run CodeHarvester in GUI mode, add the `--gui True` flag to the command:

```bash
python3 src/main.py <ROOT_DIRECTORY> --gui True
```

Navigate to `http://localhost:5043` in your web browser to interact with the application.

## Building the Binary

To compile CodeHarvester into a standalone binary for easy distribution, use PyInstaller:

```bash
pyinstaller --onefile ./src/main.py
# The binary will be located in the `dist` directory
```

## Output example

Running the command:

```bash
python3 src/main.py /home/root/code/tmp/is-emoji --extensions js yml --exclude-dirs .git
```

The output consists of all files present in the root folder "is-emoji", except for the .git folder and including all files with .js .yml extension.

![Example of the output](./assets/example_output_dark.png)

## Running Tests

To run the end-to-end tests, use:

```bash
python3 test/e2e.py
```

## Alternatives

For quick tasks, you might use terminal commands like `find` and `tree`:

Aggregate files:

```bash
find /path/to/directory -name '*.py' -print0 | xargs -0 cat > combined_files.txt
```

Generate a directory tree:

```bash
tree /path/to/directory
```
