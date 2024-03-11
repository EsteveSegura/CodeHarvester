
import unittest
import subprocess

class TestCodeHarvesterE2E(unittest.TestCase):
    def test_case_one(self):
        command = [
            'python3', 'src/main.py', './test/test_dir', 
            '--extensions', 'txt', 'py', 
            '--exclude-dirs', './exclude_this_dir', 
            '--exclude-files', './subdir2/exclude_this_file.txt'
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)

        expected_output = """
Filename: ./test/test_dir/subdir2/file3.py
```py
import random

# Generate a random integer between 1 and 10
random_int = random.randint(1, 10)
print(random_int)

```

Filename: ./test/test_dir/subdir1/file1.txt
```txt
- text
- list
- hey
```
├── subdir1
│   ├── file1.txt
│   └── file2.js
└── subdir2
    ├── exclude_this_file.txt
    └── file3.py
""".strip()

        #self.assertEqual(result.stdout.strip(), expected_output)

    def test_case_two(self):
        command = [
            'python3', 'src/main.py', './test/test_dir', 
            '--extensions', 'py', 'js', 'txt',
            '--exclude-dirs', './exclude_this_dir/', 
            '--exclude-files', './subdir2/exclude_this_file.txt'
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        print("_____________________-")
        print(result.stdout.strip())
        print("_____________________-")

        expected_output = """
Filename: ./test/test_dir/subdir2/file3.py
```py
import random

# Generate a random integer between 1 and 10
random_int = random.randint(1, 10)
print(random_int)

```

Filename: ./test/test_dir/subdir1/file2.js
```js
setTimeout(() => {
    console.log('3 segs');
}, 3000);
```

Filename: ./test/test_dir/subdir1/file1.txt
```txt
- text
- list
- hey
```
├── subdir1
│   ├── file1.txt
│   └── file2.js
└── subdir2
    ├── exclude_this_file.txt
    └── file3.py
""".strip()

        #self.assertEqual(result.stdout.strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
