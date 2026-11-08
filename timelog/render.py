"""Turns results into text for the terminal. No files and no printing."""
from datetime import date, datetime
from typing import List

from .model import Entry


def _fmt_time(time: datetime) -> str:
    """Converts a time to HH:MM."""
    return time.strftime("%H:%M")


def _format_action(prefix: str, entry: Entry) -> str:
    """Single base formatter for 'Prefix: text (HH:MM)' messages."""
    return f"{prefix}: {entry.text} ({_fmt_time(entry.time)})"


def format_duration(minutes: int) -> str:
    """Converts minutes to readable format (45 -> '45m', 65 -> '1h 05m')."""
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}h {mins:02d}m"
    return f"{mins}m"


def time_started(entry: Entry) -> str:
    """The message after `tl add`, e.g. 'Started: Team daily (09:15)'."""
    return _format_action("Started", entry)


def time_added(entry: Entry) -> str:
    """The message after `tl add -t/--time`, e.g. 'Added: Team daily (09:15)'."""
    return _format_action("Added", entry)


def note_added(entry: Entry) -> str:
    """The message after `tl note`, e.g. 'Note added: PR created (10:45)'."""
    return _format_action("Note added", entry)


def todo_added(entry: Entry) -> str:
    """The message after `tl todo`, e.g. 'Todo added: Call the client'."""
    return f"Todo added: {entry.text}"


def todo_list(day: date, entries: List[Entry]) -> str:
    """Todos of one day as a heading and a bullet list."""
    lines = [f"Todos from {day.strftime('%a %Y-%m-%d')}:"]
    lines += [f"  - {e.text}" for e in entries]
    return "\n".join(lines)


def no_todos() -> str:
    """The message when the previous day has no todos."""
    return "No todos from the previous day."


def missing_argument_error(prefix: str, argument: str, example: str) -> str:
    """Returns an error message when a required argument is missing."""
    return f"{prefix}: {argument} is missing. Usage: {example}"


def flag_not_allowed(prefix: str, flag: str) -> str:
    """Returns an error message when a flag is used somewhere it isn't allowed."""
    return f"{prefix}: flag '{flag}' is not allowed."
