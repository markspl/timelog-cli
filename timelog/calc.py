"""Calculatee Durations and totals.

Planned feature. This is needed when showing a list or current task:
- A task lasts from its `add` entry to the next `add` or `stop` entry.
- `note` entries are skipped when looking for the end of a task.
- The last task has no end. The caller passes `now`, and the task is running.
- Totals group by exact task name.
"""
from datetime import datetime
from typing import List, Optional, Tuple

from .model import Entry

def durations(entries: List[Entry], now: datetime) -> List[Tuple[Entry, Optional[int]]]:
    """Pair each entry with its duration in minutes. `None` for notes and stops."""
    raise NotImplementedError("planned for `tl list`")
 