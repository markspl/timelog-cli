import unittest
from datetime import datetime

from timelog import render
from timelog.model import Entry


def _entry(kind="add"):
    return Entry(datetime(2026, 9, 23, 9, 5), kind, "Team daily")


class RenderTest(unittest.TestCase):
    def test_format_duration(self):
        self.assertEqual(render.format_duration(0), "0m")
        self.assertEqual(render.format_duration(45), "45m")
        self.assertEqual(render.format_duration(60), "1h 00m")
        self.assertEqual(render.format_duration(65), "1h 05m")

    def test_action_messages(self):
        self.assertEqual(render.time_started(_entry()), "Started: Team daily (09:05)")
        self.assertEqual(render.time_added(_entry()), "Added: Team daily (09:05)")
        self.assertEqual(render.note_added(_entry("note")), "Note added: Team daily (09:05)")

    def test_errors(self):
        self.assertEqual(
            render.missing_argument_error("tl add", "description", "tl add <description>"),
            "tl add: description is missing. Usage: tl add <description>",
        )
        self.assertEqual(render.flag_not_allowed("tl note", "-t"), "tl note: flag '-t' is not allowed.")


if __name__ == "__main__":
    unittest.main()
