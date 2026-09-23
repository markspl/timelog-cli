"""The only module that touches files (read/write).

Data lives in one file per day: ~/.timelog/<yyyy-mm-dd>.tsv
"""
from datetime import date
from pathlib import Path

from .model import Entry

def data_dir() -> Path:
    return Path.home() / ".timelog"

def day_file(day: date) -> Path:
    return data_dir() / (day.isoformat() + ".tsv")

def append_entry(entry: Entry) -> None:
    """Add one line to the file of the entry's date. Creates the folder and file if needed."""
    path = day_file(entry.time.date())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(entry.to_line() + "\n")
