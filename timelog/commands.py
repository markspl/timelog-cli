"""One function per command. Each one connects storage, model, calc and render.

A command gets the words after its name and returns the exit code.
"""
import re
import sys
from datetime import datetime, timedelta
from typing import List

from . import render, storage
from .model import Entry

TIME_FLAGS = {"-t", "--time"}


def _now() -> datetime:
    return datetime.now().replace(second=0, microsecond=0)


def _get_time_flag(args):
    """Return (time_string_or_None, remaining_args), pulling out -t/--time and its value.
    The flag is recognized only as the first argument"""
    if args and args[0] in (TIME_FLAGS):
        if len(args) < 2:
            print(f"tl add: {args[0]} needs a value, e.g. {args[0]} 14:30", file=sys.stderr)
            return None, None
        return args[1], args[2:]
    return None, args


def _parse_time_flag(value: str, now: datetime) -> datetime:
    """'11:30' -> today at 11:30. '1h15m', '1h', '5m' -> now minus the duration."""
    if ":" in value:
        hh, mm = value.split(":")
        return now.replace(hour=int(hh), minute=int(mm))

    # check string match pattern ?(digits)h?(digits)m, e.g. "1h30m"
    # saves as Match object
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?", value)
    if not m or not value:
        raise ValueError(value)

    # groups() returns a tuple of all captured groups
    hours, minutes = (int(g) if g else 0 for g in m.groups())
    return now - timedelta(hours=hours, minutes=minutes)


def add(args: List[str]) -> int:
    """tl add [-t|--time <value>] <description>: start a task.

    Task starts when a command is sent, if no flag -t/--time.
    With the flag, value is either a time (12:00) or how long ago it started (1h30m).

    Examples:
        tl add Explaining what 67 means
        tl add -t 14:30 Meeting
        tl add --time 1h30m Long lunch
    """
    time_str, rest = _get_time_flag(args)
    if time_str is None and rest is None:
        return 1

    when = _now()
    if time_str:
        try:
            when = _parse_time_flag(time_str, now=when)
        except ValueError:
            print(f"tl add: can't parse time flag '{time_str}'. Use HH:MM or e.g. 1h5m, 15m", file=sys.stderr)
            return 1

    entry = Entry(time=when, type="add", text=" ".join(rest))
    if not entry.text:
        print(
            render.missing_argument_error("tl add", "description", "tl add <description>"),
            file=sys.stderr
        )
        return 1

    storage.append_entry(entry)
    if time_str:
        print(render.time_added(entry))
    else:
        print(render.time_started(entry))

    return 0


def note(args: List[str]) -> int:
    """tl note <note>: add a note."""
    if args and args[0] in (TIME_FLAGS):
        print(render.flag_not_allowed("tl note", args[0]), file=sys.stderr)
        return 1

    entry = Entry(time=_now(), type="note", text=" ".join(args[0:]))

    if not entry.text:
        print(
            render.missing_argument_error("tl note", "description", "tl note <description>"),
            file=sys.stderr
        )
        return 1

    storage.append_entry(entry)
    print(render.note_added(entry))

    return 0
