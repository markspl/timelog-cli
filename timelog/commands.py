"""One function per command. Each one connects storage, model, calc and render.

A command gets the words after its name and returns the exit code.
"""
import sys
from datetime import datetime
from typing import List

from . import render, storage
from .model import Entry

def _now() -> datetime:
    return datetime.now().replace(second=0, microsecond=0)

def _get_time_flag(args):
    """Return (time_string_or_None, remaining_args), pulling out -t/--time and its value.
    The flag is recognized only as the first argument"""
    if args and args[0] in ("-t", "--time"):
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
        print("tl add: description is missing. Usage: tl add <description>", file=sys.stderr)
        return 1

    storage.append_entry(entry)
    if time_str:
        print(render.time_added(entry))
    else:
        print(render.started(entry))

    return 0
