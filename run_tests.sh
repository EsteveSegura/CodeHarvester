#!/bin/bash

# Function to add 'src.' to imports
add_src_prefix() {
    find ./src -type f -name "*.py" -exec sed -i 's/^import file_manipulation/import src.file_manipulation/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^import utils/import src.utils/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^import gui/import src.gui/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^from file_manipulation/from src.file_manipulation/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^from utils/from src.utils/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^from gui/from src.gui/' {} \;
}

# Function to remove 'src.' from imports
remove_src_prefix() {
    find ./src -type f -name "*.py" -exec sed -i 's/^import src.file_manipulation/import file_manipulation/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^import src.utils/import utils/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^import src.gui/import gui/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^from src.file_manipulation/from file_manipulation/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^from src.utils/from utils/' {} \;
    find ./src -type f -name "*.py" -exec sed -i 's/^from src.gui/from gui/' {} \;
}

# Add 'src.' prefix to imports
echo "Adding 'src.' prefix to imports..."
add_src_prefix

# Run the tests
echo "Running tests..."
python3 -m unittest discover -s test -p "test_*.py"

# Remove 'src.' prefix from imports
echo "Removing 'src.' prefix from imports..."
remove_src_prefix

echo "Done."
