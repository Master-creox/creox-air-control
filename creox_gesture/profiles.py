"""Target profiles — one gesture set, different target windows.

Phase 1 (slides_music) is unchanged. Phase 2 (suit) reuses the same
gestures for the Creox Suit HUD (suit_hud.html, standalone, simulated
systems) — chat-style log scroll + system navigation TOGETHER.
Air Control stays standalone and is NOT an Aegis project: it only
sends generic key/click/scroll actions to the active window.
Suit HUD navigation uses Tab / Shift+Tab (focus order in the browser
window); log scroll uses mouse-wheel scroll.
Safety: gestures only mean something when the target window is the
active one — the user focuses the Suit HUD first, then turns mode ON.
"""
from __future__ import annotations

PROFILES = {
    "slides_music": {
        "move": "move",
        "click": "click",
        "next": "next",
        "prev": "prev",
        "volume_up": "volume_up",
        "volume_down": "volume_down",
        "palm_pause": "palm_pause",
    },
    "suit": {
        "move": "move",          # cursor over Suit HUD
        "click": "click",        # click a system button / toggle in Suit HUD
        "next": "panel_next",   # Tab: next system / focus item
        "prev": "panel_prev",   # Shift+Tab: previous system / focus item
        "volume_up": "scroll_up",    # wheel up: log scroll up
        "volume_down": "scroll_down",  # wheel down: log scroll down
        "palm_pause": "palm_pause",
    },
    # Legendary: browser tabs + media control, same 6 gestures.
    "browser": {
        "move": "move",
        "click": "click",
        "next": "next_tab",    # Ctrl+Tab
        "prev": "prev_tab",    # Ctrl+Shift+Tab
        "volume_up": "scroll_up",
        "volume_down": "scroll_down",
        "palm_pause": "palm_pause",
    },
    "media": {
        "move": "move",
        "click": "media_play_pause",  # pinch = play/pause in media profile
        "next": "media_next",
        "prev": "media_prev",
        "volume_up": "volume_up",
        "volume_down": "volume_down",
        "palm_pause": "palm_pause",
    },
}


def translate(profile, gesture):
    """Map a raw gesture to the action for this profile, or None."""
    return PROFILES.get(profile, {}).get(gesture)
