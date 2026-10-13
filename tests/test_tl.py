import contextlib
import io
import unittest

import tl
from timelog import __version__


def run_main(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tl.main(argv)
    return code, out.getvalue(), err.getvalue()


class MainTest(unittest.TestCase):
    def test_help(self):
        for argv in ([], ["help"], ["-h"], ["--help"]):
            with self.subTest(argv=argv):
                code, out, _ = run_main(argv)
                self.assertEqual(code, 0)
                self.assertIn("Usage: tl <command>", out)

    def test_version(self):
        self.assertEqual(run_main(["version"]), (0, "timelog-cli " + __version__ + "\n", ""))

    def test_unknown_command(self):
        code, out, err = run_main(["frobnicate"])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("unknown command 'frobnicate'", err)

    def test_planned_command(self):
        code, _, err = run_main(["list"])
        self.assertEqual(code, 1)
        self.assertIn("not implemented yet", err)

    def test_planned_commands_are_not_registered(self):
        self.assertFalse(tl.PLANNED & set(tl.COMMANDS))


if __name__ == "__main__":
    unittest.main()
