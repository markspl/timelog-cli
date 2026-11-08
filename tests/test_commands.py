import contextlib
import io
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from timelog import commands

NOW = datetime(2026, 9, 23, 12, 0)


class CommandTestCase(unittest.TestCase):
    """Runs commands against a temp home dir and a frozen clock."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        for patcher in (
            mock.patch.dict(os.environ, {"HOME": str(self.home), "USERPROFILE": str(self.home)}),
            mock.patch.object(commands, "_now", return_value=NOW),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_cmd(self, func, args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = func(args)
        return code, out.getvalue(), err.getvalue()

    def day_file(self, day="2026-09-23"):
        return self.home / ".timelog" / (day + ".tsv")

    def lines(self, day="2026-09-23"):
        return self.day_file(day).read_text(encoding="utf-8").splitlines()


class ParseTimeFlagTest(unittest.TestCase):
    def test_clock_time(self):
        self.assertEqual(commands._parse_time_flag("09:30", NOW), datetime(2026, 9, 23, 9, 30))

    def test_clock_time_later_today_is_allowed(self):
        # logging what will happen later today is intended
        self.assertEqual(commands._parse_time_flag("23:30", NOW), datetime(2026, 9, 23, 23, 30))

    def test_durations(self):
        parse = commands._parse_time_flag
        self.assertEqual(parse("1h30m", NOW), datetime(2026, 9, 23, 10, 30))
        self.assertEqual(parse("1h", NOW), datetime(2026, 9, 23, 11, 0))
        self.assertEqual(parse("15m", NOW), datetime(2026, 9, 23, 11, 45))

    def test_crossing_midnight_goes_to_previous_day(self):
        self.assertEqual(commands._parse_time_flag("13h", NOW), datetime(2026, 9, 22, 23, 0))

    def test_invalid(self):
        for bad in ("", "abc", "1x", "ab:cd", "25:00", "1:2:3"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                commands._parse_time_flag(bad, NOW)


class GetTimeFlagTest(unittest.TestCase):
    def test_no_flag(self):
        self.assertEqual(commands._get_time_flag(["a", "b"]), (None, ["a", "b"]))

    def test_flag_only_first(self):
        self.assertEqual(commands._get_time_flag(["a", "-t", "5m"]), (None, ["a", "-t", "5m"]))

    def test_short_and_long(self):
        self.assertEqual(commands._get_time_flag(["-t", "5m", "x"]), ("5m", ["x"]))
        self.assertEqual(commands._get_time_flag(["--time", "5m", "x"]), ("5m", ["x"]))

    def test_missing_value(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(commands._get_time_flag(["-t"]), (None, None))

    def test_missing_value_uses_prefix(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            commands._get_time_flag(["-t"], "tl note")
        self.assertTrue(err.getvalue().startswith("tl note: -t needs a value"))


class AddTest(CommandTestCase):
    def test_add_now(self):
        code, out, _ = self.run_cmd(commands.add, ["Team", "daily"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Started: Team daily (12:00)\n")
        self.assertEqual(self.lines(), ["2026-09-23 12:00\tadd\tTeam daily"])

    def test_add_with_clock_time(self):
        code, out, _ = self.run_cmd(commands.add, ["-t", "09:30", "Meeting"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Added: Meeting (09:30)\n")
        self.assertEqual(self.lines(), ["2026-09-23 09:30\tadd\tMeeting"])

    def test_add_with_duration(self):
        self.run_cmd(commands.add, ["--time", "1h30m", "Lunch"])
        self.assertEqual(self.lines(), ["2026-09-23 10:30\tadd\tLunch"])

    def test_backdated_entry_appended_at_end(self):
        self.run_cmd(commands.add, ["Later"])
        self.run_cmd(commands.add, ["-t", "08:00", "Earlier"])
        self.assertEqual(
            self.lines(),
            ["2026-09-23 12:00\tadd\tLater", "2026-09-23 08:00\tadd\tEarlier"],
        )

    def test_previous_day_is_rejected(self):
        code, out, err = self.run_cmd(commands.add, ["-t", "13h", "Late"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("previous day", err)
        self.assertFalse((self.home / ".timelog").exists())

    def test_bad_time_flag(self):
        code, out, err = self.run_cmd(commands.add, ["-t", "nope", "x"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("can't parse time flag 'nope'", err)
        self.assertFalse(self.day_file().exists())

    def test_flag_without_value(self):
        code, _, err = self.run_cmd(commands.add, ["-t"])
        self.assertEqual(code, 1)
        self.assertIn("needs a value", err)

    def test_missing_description(self):
        for args in ([], ["-t", "5m"], ["  "]):
            with self.subTest(args=args):
                code, out, err = self.run_cmd(commands.add, args)
                self.assertEqual(code, 1)
                self.assertEqual(out, "")
                self.assertIn("description is missing", err)
        self.assertFalse(self.day_file().exists())


class NoteTest(CommandTestCase):
    def test_note(self):
        code, out, _ = self.run_cmd(commands.note, ["PR", "created"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Note added: PR created (12:00)\n")
        self.assertEqual(self.lines(), ["2026-09-23 12:00\tnote\tPR created"])

    def test_note_with_clock_time(self):
        code, out, _ = self.run_cmd(commands.note, ["-t", "09:30", "Decided"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Note added: Decided (09:30)\n")
        self.assertEqual(self.lines(), ["2026-09-23 09:30\tnote\tDecided"])

    def test_note_previous_day_is_rejected(self):
        code, _, err = self.run_cmd(commands.note, ["-t", "13h", "Late"])
        self.assertEqual(code, 1)
        self.assertIn("tl note: '13h' is on a previous day", err)
        self.assertFalse((self.home / ".timelog").exists())

    def test_note_with_duration(self):
        self.run_cmd(commands.note, ["--time", "20m", "Called"])
        self.assertEqual(self.lines(), ["2026-09-23 11:40\tnote\tCalled"])

    def test_bad_time_flag(self):
        code, out, err = self.run_cmd(commands.note, ["-t", "nope", "x"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("tl note: can't parse time flag 'nope'", err)
        self.assertFalse(self.day_file().exists())

    def test_flag_without_value(self):
        code, _, err = self.run_cmd(commands.note, ["-t"])
        self.assertEqual(code, 1)
        self.assertIn("tl note: -t needs a value", err)

    def test_flag_without_text(self):
        for args in (["-t", "5m"], ["-t", "5m", "  "]):
            with self.subTest(args=args):
                code, out, err = self.run_cmd(commands.note, args)
                self.assertEqual(code, 1)
                self.assertEqual(out, "")
                self.assertIn("description is missing", err)
        self.assertFalse(self.day_file().exists())

    def test_missing_text(self):
        code, _, err = self.run_cmd(commands.note, [])
        self.assertEqual(code, 1)
        self.assertIn("description is missing", err)
