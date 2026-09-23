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


def add(args: List[str]) -> int:
    """tl add <description>: start a task now."""
    entry = Entry(time=_now(), type="add", text=" ".join(args))
    if not entry.text:
        print("tl add: description is missing. Usage: tl add <description>", file=sys.stderr)
        return 1
    storage.append_entry(entry)
    print(render.started(entry))
    return 0
 