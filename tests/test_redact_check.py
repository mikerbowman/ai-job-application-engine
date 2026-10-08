import tempfile
import unittest
from pathlib import Path

from scripts.redact_check import scan


class RedactCheckTests(unittest.TestCase):
    def test_clean_file_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "example.md").write_text("A public workflow example.", encoding="utf-8")
            self.assertEqual(scan(root), [])

    def test_email_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "candidate.md").write_text("Email: candidate@example.com", encoding="utf-8")
            self.assertTrue(any("email address" in item for item in scan(root)))

    def test_secret_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config.yaml").write_text(
                "api_key: abcdefghijklmnopqrstuvwxyz123456", encoding="utf-8"
            )
            self.assertTrue(any("API token" in item for item in scan(root)))


if __name__ == "__main__":
    unittest.main()

