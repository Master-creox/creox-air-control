"""Gesture history — a small, honest log of what actually fired.

The app records every fired action (time, gesture, action, whether
pyautogui really performed it) in a ring buffer, and appends the same
events to a JSONL file when a log path is configured. This is the
debugging record: if a gesture misfires, the log shows exactly what
the app saw and did, instead of a guess from memory.

The log file is local-only (own laptop), capped by max_events in
memory; the file itself is appended, never uploaded anywhere.
"""
from __future__ import annotations

import json
import time
from collections import deque
from pathlib import Path


class GestureHistory:
    def __init__(self, max_events: int = 200, log_file: str | Path | None = None):
        self.events: deque = deque(maxlen=max_events)
        self.log_file = Path(log_file) if log_file else None

    def record(self, gesture: str, action: str | None, performed: bool) -> dict:
        event = {
            "time": time.strftime("%H:%M:%S"),
            "gesture": gesture,
            "action": action,
            "performed": performed,
        }
        self.events.append(event)
        if self.log_file:
            try:
                with self.log_file.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(event) + "\n")
            except OSError:
                pass  # Logging must never break gesture control.
        return event

    def last(self, count: int = 10) -> list:
        return list(self.events)[-count:]
