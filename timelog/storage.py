"""The only module that touches files (read/write).

Data lives in one file per day: ~/.timelog/<yyyy-mm-dd>.tsv
"""
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

from .model import Entry


def _data_dir() -> Path:
    return Path.home() / ".timelog"


def _day_file(day: date) -> Path:
    return _data_dir() / (day.isoformat() + ".tsv")


def day_exists(day: date) -> bool:
    """True if anything has been logged on that day."""
    return _day_file(day).exists()


def _read_entries(day: date) -> List[Entry]:
    """All entries of one day in file order. Lines that can't be parsed (hand edits) are skipped."""
    entries = []
    with _day_file(day).open(encoding="utf-8") as f:
        for line in f:
            try:
                entries.append(Entry.from_line(line))
            except ValueError:
                continue
    return entries


def _previous_day(before: date) -> Optional[date]:
    """The latest day earlier than `before` that has a log file, or None."""
    days = []
    if _data_dir().is_dir():
        for path in _data_dir().glob("*.tsv"):
            try:
                day = date.fromisoformat(path.stem)
            except ValueError:
                continue
            if day < before:
                days.append(day)
    return max(days, default=None)


def previous_todos(before: date) -> Tuple[Optional[date], List[Entry]]:
    """The todos of the most recent day earlier than `before`, as (that day, todos).

    Only that one day is looked at, so a day off between does not hide its todos,
    but todos from older days are not carried further."""
    day = _previous_day(before)
    if day is None:
        return None, []
    return day, [e for e in _read_entries(day) if e.type == "todo"]


def append_entry(entry: Entry) -> None:
    """Add one add-type line to the file of the entry's date. Creates the folder and file if needed."""
    path = _day_file(entry.time.date())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(entry.to_line() + "\n")
