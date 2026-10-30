"""User-tunable settings for Creox Air Control (Legendary package).

Settings live in an optional JSON file next to the package
(``air_control_settings.json`` in the project root). Missing file,
bad JSON, unknown keys, or out-of-range values never crash the app:
every value falls back to its safe default, and the app prints which
file it loaded (or that it used defaults).

This is calibration, not magic: a smaller pinch threshold makes
pinches easier to trigger (and easier to trigger by accident); a
larger swipe threshold needs a bigger hand movement. Defaults are
the values Phase 1 was laptop-verified with.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

DEFAULTS = {
    "debounce_seconds": 0.3,
    "pinch_threshold": 0.05,
    "swipe_threshold": 0.25,
    "swipe_window": 8,
    "swipe_cooldown_frames": 10,
    "min_hand_detection_confidence": 0.7,
    "min_tracking_confidence": 0.7,
    "gesture_log_file": "gesture_log.jsonl",
    "gesture_log_max_events": 200,
}

RANGES = {
    "debounce_seconds": (0.05, 2.0),
    "pinch_threshold": (0.02, 0.15),
    "swipe_threshold": (0.1, 0.6),
    "swipe_window": (4, 20),
    "swipe_cooldown_frames": (0, 60),
    "min_hand_detection_confidence": (0.3, 0.95),
    "min_tracking_confidence": (0.3, 0.95),
    "gesture_log_max_events": (10, 1000),
}


@dataclass
class Settings:
    debounce_seconds: float = 0.3
    pinch_threshold: float = 0.05
    swipe_threshold: float = 0.25
    swipe_window: int = 8
    swipe_cooldown_frames: int = 10
    min_hand_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.7
    gesture_log_file: str = "gesture_log.jsonl"
    gesture_log_max_events: int = 200
    source: str = field(default="defaults", repr=False)

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Settings":
        """Load settings from JSON, or defaults when anything is wrong."""
        candidate = Path(path) if path else (
            Path(__file__).resolve().parent.parent / "air_control_settings.json"
        )
        if not candidate.is_file():
            return cls()
        try:
            raw = json.loads(candidate.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return cls()
        if not isinstance(raw, dict):
            return cls()
        values = {}
        for key, default in DEFAULTS.items():
            if key not in raw:
                continue
            value = raw[key]
            if key in RANGES and isinstance(value, (int, float)):
                low, high = RANGES[key]
                if not (low <= value <= high):
                    continue
            if key == "gesture_log_file" and not isinstance(value, str):
                continue
            if key in ("swipe_window", "swipe_cooldown_frames",
                       "gesture_log_max_events") and not isinstance(value, int):
                continue
            values[key] = value
        return cls(**values, source=str(candidate))
