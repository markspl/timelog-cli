"""Turns results into text for the terminal. No files and no printing."""
from datetime import datetime

from .model import Entry

def _get_time_str(time: datetime) -> str:
    """Converts and returns time as HH:MM."""
    return time.strftime("%H:%M")

def _format_action(prefix: str, entry: Entry) -> str:
    """Single base formatter"""
    return f"{prefix}: {entry.text} ({_get_time_str(entry.time)})"

def format_duration(minutes: int) -> str:
    """Converts number to readable format (45 -> '45m', 65 -> '1h 05m')."""
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}h {mins:02d}m"
    return f"{mins}m"

def time_started(entry: Entry) -> str:
    """The message after `tl add`, e.g. 'Started: Team daily (09:15)'."""
    return _format_action("Started", entry)

def time_added(entry: Entry) -> str:
    """The message after `tl add (-t|--time)`, e.g. 'Added: Team daily (09:15)'."""
    return _format_action("Added", entry)

def note_added(entry: Entry) -> str:
    """The message after `tl note`, e.g. 'Added note: PR created (10:45)'."""
    return _format_action("Note added", entry)

def missing_argument_error(prefix: str, argument: str, example: str) -> str:
    """Returns an error message when a required argument is missing."""
    return f"{prefix}: {argument} is missing. Usage: {example}"

def flag_not_allowed(prefix: str, flag: str) -> str:
    """Returns an error message when a flag is."""
    return f"{prefix}: Flag '{flag}' is not allowd."
