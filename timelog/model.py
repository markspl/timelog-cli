"""An entry is one record in the log, for example one `tl add`.

This file turns an entry into a line of text for the day file, and a line back into an entry.

A line has three fields, separated by tab characters: date and time, type, text.
For example (<TAB> is a real tab character):

    2026-09-23 09:15<TAB>add<TAB>Team daily
"""
from dataclasses import dataclass
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M"
TYPES = ("add",)  # planned more types later (e.g. note, stop)

def clean_text(text: str) -> str:
    """One entry is one line: tabs and newlines become spaces, extra spaces are collapsed."""
    return " ".join(text.split())

@dataclass
class Entry:
    time: datetime
    type: str
    text: str

    def __post_init__(self):
        if self.type not in TYPES:
            raise ValueError("unknown entry type: %r" % self.type)
        self.text = clean_text(self.text)

    def to_line(self) -> str:
        return "\t".join([self.time.strftime(TIME_FORMAT), self.type, self.text])

    @classmethod
    def from_line(cls, line: str) -> "Entry":
        fields = line.rstrip("\n").split("\t", 2)
        if len(fields) != 3:
            raise ValueError("expected 3 tab-separated fields: %r" % line)
        time = datetime.strptime(fields[0], TIME_FORMAT)
        return cls(time=time, type=fields[1], text=fields[2])
