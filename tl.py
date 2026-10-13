#!/usr/bin/env python3
"""tl - simple time/task logging on the command line.

This file only reads the arguments and picks a command.
The work is done in the `timelog` package.
"""
import sys

from timelog import __version__, commands


USAGE = """\
timelog-cli {version} - log what you work on

Usage: tl <command> [text]

Commands:
  add [-t | --time <value>] <description>   start a task now, or at <value>
  note <text>                               add a note to today's log
  version                                   show the version
  help                                      show this help

Time values for -t / --time:
  14:30            today at that time
  1h30m, 1h, 15m   how long ago the task started
""".format(version=__version__)

COMMANDS = {
    "add": commands.add,
    "note": commands.note,
}

# Planned commands from README
PLANNED = {"list", "now", "edit", "stop", "delete", "nonwork"}


def main(argv):
    if not argv or argv[0] in ("help", "-h", "--help"):
        print(USAGE, end="")
        return 0

    name, args = argv[0], argv[1:]

    if name == "version":
        print("timelog-cli " + __version__)
        return 0

    handler = COMMANDS.get(name)
    if handler:
        return handler(args)

    if name in PLANNED:
        print(f"tl: '{name}' is not implemented yet.", file=sys.stderr)
    else:
        print(f"tl: unknown command '{name}'. Try 'tl help'.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
