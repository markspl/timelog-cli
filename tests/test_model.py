import unittest
from datetime import datetime

from timelog.model import Entry, clean_text


class CleanTextTest(unittest.TestCase):
    def test_collapses_whitespace_and_newlines(self):
        self.assertEqual(clean_text("  a \t b\n\nc  "), "a b c")


class EntryTest(unittest.TestCase):
    def test_unknown_type_rejected(self):
        with self.assertRaises(ValueError):
            Entry(datetime(2026, 9, 23, 9, 15), "bogus", "x")

    def test_text_is_normalized(self):
        e = Entry(datetime(2026, 9, 23, 9, 15), "add", "a\tb\nc")
        self.assertEqual(e.text, "a b c")

    def test_to_line(self):
        e = Entry(datetime(2026, 9, 23, 9, 15), "add", "Team daily")
        self.assertEqual(e.to_line(), "2026-09-23 09:15\tadd\tTeam daily")

    def test_round_trip(self):
        e = Entry(datetime(2026, 9, 23, 9, 15), "note", "PR created")
        self.assertEqual(Entry.from_line(e.to_line() + "\n"), e)

    def test_from_line_wrong_field_count(self):
        with self.assertRaises(ValueError):
            Entry.from_line("2026-09-23 09:15\tadd")

    def test_from_line_bad_time(self):
        with self.assertRaises(ValueError):
            Entry.from_line("yesterday\tadd\tx")

    def test_from_line_unknown_type(self):
        with self.assertRaises(ValueError):
            Entry.from_line("2026-09-23 09:15\tstop\tx")


if __name__ == "__main__":
    unittest.main()
