"""Pure gesture classification from MediaPipe-style hand landmarks.

Input: a list of 21 (x, y) points in MediaPipe Hands order
(0 wrist, 4 thumb tip, 8 index tip, 12 middle tip, 16 ring tip,
20 pinky tip, 5/9/13/17 finger MCPs, 6/10/14/18 finger PIPs).
No camera, no MediaPipe import here — so this module is unit-testable
anywhere, including a headless VM.

A finger counts as extended when its tip is clearly farther from the
wrist than its PIP joint. Thresholds are deliberately conservative:
an unclear hand returns None (no action) instead of a guessed gesture.
"""
from __future__ import annotations

import math
from collections import deque

TIP = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
PIP = {"index": 6, "middle": 10, "ring": 14, "pinky": 18}


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _finger_extended(lm, finger):
    wrist = lm[0]
    return _dist(lm[TIP[finger]], wrist) > _dist(lm[PIP[finger]], wrist) * 1.15


def classify(lm):
    """Return one of: move, click, palm_pause, or None.

    Swipe gestures (next/prev/volume) are temporal — they need motion
    over frames — so they live in SwipeDetector, not here.
    """
    if lm is None or len(lm) != 21:
        return None
    try:
        ext = {f: _finger_extended(lm, f) for f in ("index", "middle", "ring", "pinky")}
    except (TypeError, IndexError):
        return None
    # Pinch first: thumb tip very close to index tip.
    if _dist(lm[4], lm[8]) < 0.05:
        return "click"
    # Open palm: all four fingers extended.
    if all(ext.values()):
        return "palm_pause"
    # Index only: cursor move.
    if ext["index"] and not (ext["middle"] or ext["ring"] or ext["pinky"]):
        return "move"
    # Fist / unclear / anything else: no action, never guess.
    return None


class SwipeDetector:
    """Detect a fast dominant-axis swipe of the index fingertip.

    Returns next / prev / volume_up / volume_down, or None.
    A swipe must exceed the distance threshold within the recent
    window, then a cooldown blocks repeats until the hand settles.
    """

    def __init__(self, window=8, threshold=0.25, cooldown_frames=10):
        self.history = deque(maxlen=window)
        self.threshold = threshold
        self.cooldown = 0
        self.cooldown_frames = cooldown_frames

    def update(self, tip):
        """Feed one (x, y) index-tip point per frame."""
        if self.cooldown > 0:
            self.cooldown -= 1
            self.history.clear()
            return None
        self.history.append(tip)
        if len(self.history) < self.history.maxlen:
            return None
        dx = self.history[-1][0] - self.history[0][0]
        dy = self.history[-1][1] - self.history[0][1]
        result = None
        if abs(dx) >= self.threshold and abs(dx) >= abs(dy):
            result = "next" if dx > 0 else "prev"
        elif abs(dy) >= self.threshold and abs(dy) > abs(dx):
            # Image y grows downward: hand moving up = volume up.
            result = "volume_up" if dy < 0 else "volume_down"
        if result:
            self.cooldown = self.cooldown_frames
            self.history.clear()
        return result
