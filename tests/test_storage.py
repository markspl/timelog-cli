import unittest

from tests.test_commands import NOW, CommandTestCase
from timelog import storage
from timelog.model import Entry


class StorageTest(CommandTestCase):
    def test_appends_and_creates_dir(self):
        storage.append_entry(Entry(NOW, "add", "one"))
        storage.append_entry(Entry(NOW, "note", "two"))
        self.assertEqual(self.lines(), ["2026-09-23 12:00\tadd\tone", "2026-09-23 12:00\tnote\ttwo"])

    def test_uses_lf_line_endings(self):
        storage.append_entry(Entry(NOW, "add", "one"))
        self.assertNotIn(b"\r", self.day_file().read_bytes())
