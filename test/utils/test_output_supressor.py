import unittest
import sys
from io import StringIO
from src.utils.output_supressor import DisablePrint

class TestOutputSupressor(unittest.TestCase):

    def test_disable_print(self):
        # Save the original values of stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        # Create buffers to capture stdout and stderr
        captured_stdout = StringIO()
        captured_stderr = StringIO()

        # Redirect stdout and stderr to the buffers
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        with DisablePrint():
            print("This should not appear in stdout")
            print("This should not appear in stderr", file=sys.stderr)

        # Restore stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Ensure stdout and stderr are empty
        self.assertEqual(captured_stdout.getvalue(), "")
        self.assertEqual(captured_stderr.getvalue(), "")

    def test_restore_print(self):
        # Save the original values of stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        # Create buffers to capture stdout and stderr
        captured_stdout = StringIO()
        captured_stderr = StringIO()

        with DisablePrint():
            pass  # Do nothing inside the context

        # Redirect stdout and stderr to the buffers
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        # Print something after exiting the context
        print("This should appear in stdout")
        print("This should appear in stderr", file=sys.stderr)

        # Restore stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Ensure stdout and stderr contain the printed messages
        self.assertEqual(captured_stdout.getvalue().strip(), "This should appear in stdout")
        self.assertEqual(captured_stderr.getvalue().strip(), "This should appear in stderr")

if __name__ == '__main__':
    unittest.main()
