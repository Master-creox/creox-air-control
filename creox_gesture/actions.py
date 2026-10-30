"""Gesture -> action mapping for Phase 1 (slides + music only).

Actions are returned as plain names first. The webcam app turns them
into key events only when pyautogui is installed; without it, the app
prints the action instead of pressing anything. This keeps the
allowlist visible in one place: nothing outside this dict can fire.
"""
from __future__ import annotations

# gesture -> (human description, key to press, if pyautogui is present)
ACTIONS = {
    "move": ("Move cursor to hand position", None),
    "click": ("Click / select", "click"),
    "next": ("Next slide / next song", "right"),
    "prev": ("Previous slide / previous song", "left"),
    "volume_up": ("Volume up", "volumeup"),
    "volume_down": ("Volume down", "volumedown"),
    "palm_pause": ("Pause gestures while palm is held", None),
    # Phase 2 (Suit HUD): log scroll + system navigation, same gestures.
    "scroll_up": ("Scroll up (log)", "scroll_up"),
    "scroll_down": ("Scroll down (log)", "scroll_down"),
    "panel_next": ("Next panel / focus item (Tab)", "tab"),
    "panel_prev": ("Previous panel / focus item (Shift+Tab)", "shift+tab"),
}


def describe(gesture):
    """Human description for a gesture, or None for unknown gestures."""
    entry = ACTIONS.get(gesture)
    return entry[0] if entry else None


def fire(gesture):
    """Perform the action if possible; always return its description.

    Returns (description, performed_bool). performed is False when
    pyautogui is missing (dry-run: print only) or the gesture has no
    key action (move / pause are handled by the app, not a keypress).
    """
    entry = ACTIONS.get(gesture)
    if entry is None:
        return (None, False)
    description, key = entry
    if key is None:
        return (description, False)
    try:
        import pyautogui
    except ImportError:
        return (description, False)
    if key == "click":
        pyautogui.click()
    elif key == "scroll_up":
        pyautogui.scroll(5)
    elif key == "scroll_down":
        pyautogui.scroll(-5)
    elif key == "shift+tab":
        pyautogui.hotkey("shift", "tab")
    else:
        pyautogui.press(key)
    return (description, True)
