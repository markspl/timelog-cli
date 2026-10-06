"""One function per command. Each one connects storage, model, calc and render.

A command gets the words after its name and returns the exit code.
"""
import sys
from datetime import datetime
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

def add(args: List[str]) -> int:
    """tl add [-t HH:MM | --time HH:MM] <description>: start a task, now or at a given time."""
    time_str, rest = _get_time_flag(args)
    if time_str is None and rest is None:
        return 1

    when = _now()
    if time_str:
        try:
            when = when.replace(
                hour=int(time_str.split(":")[0]),
                minute=int(time_str.split(":")[1]),
            )
        except ValueError:
            print(f"tl add: {args[0]} needs HH:MM, e.g. 14:30", file=sys.stderr)
            return 1

    entry = Entry(time=when, type="add", text=" ".join(args[2:] if time_str else args[0:]))
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
        print(render.flag_not_allowed("tl note", args[0]))
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
