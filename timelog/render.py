"""Turns results into text for the terminal. No files and no printing."""
from .model import Entry

def format_duration(minutes: int) -> str:
    """Converts number to readable format (45 -> '45m', 65 -> '1h 05m')"""
    hours, mins = divmod(minutes, 60)
    if hours:
        return "%dh %02dm" % (hours, mins)
    return "%dm" % mins

def started(entry: Entry) -> str:
    """The message after `tl add`, e.g. 'Started: Team daily (09:15)'."""
    return "Started: %s (%s)" % (entry.text, entry.time.strftime("%H:%M"))
