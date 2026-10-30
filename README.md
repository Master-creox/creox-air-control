# Creox Air Control — Camera, Standalone

Iron Man-style hand-gesture control for your own laptop, via its webcam.
Standalone project — not an Aegis Prime module.

## Phase 1 scope (locked blueprint, 2026-10-30)
- Route: laptop webcam, MediaPipe Hands
- First target: laptop slides + music only
- Safety: gesture mode is explicitly ON/OFF (`G` key or button in the
  preview window). Never always-on. Open-palm hold pauses gestures.
  Only the allowlisted actions in `creox_gesture/actions.py` can fire.
  No file, system, or other-device actions in Phase 1.

## Gestures (6)
| Gesture | Action |
|---|---|
| Index finger move | Move cursor |
| Pinch (thumb + index) | Click / select |
| Swipe right | Next slide / next song |
| Swipe left | Previous slide / previous song |
| Hand up | Volume up |
| Hand down | Volume down |
| Open palm hold | Pause gestures |

## Run on your laptop (guide-only, tests on his laptop only)
```powershell
python -m pip install -r requirements.txt
python -m creox_gesture.app
```
**One extra file first (MediaPipe 1.x):** download
`hand_landmarker.task` from
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
and put it in the `creox_gesture/` folder. Without it the app prints
exactly where to put it instead of crashing. This file is NOT in the
repo because binary files cannot be pushed by the Muse app.
Press `G` to toggle mode ON, `Q` to quit. Mode starts OFF on purpose.
If OpenCV / MediaPipe are missing, the app says so plainly instead of
crashing. No camera on a headless VM — the classifier itself is tested
without a camera (see below).

## Tests (no camera needed)
```powershell
python -m unittest discover -s tests -t .
```
Synthetic hands cover: open palm → pause, index only → move,
pinch → click, fist → nothing, unclear hand → nothing,
right swipe → next, left swipe → prev, small movement → nothing,
plus the action allowlist.

## Files
- `creox_gesture/gestures.py` — pure classifier + swipe detector (no camera import)
- `creox_gesture/actions.py` — the only allowlisted actions
- `creox_gesture/app.py` — webcam loop + preview window
- `tests/test_gestures.py` — 9 unittest cases
- `BLUEPRINT.md` — the locked blueprint

## Later phases (not started)
Aegis HUD control, phone control, ESP32 wristband version — only when
Akash asks, in that order of discussion, not by default.
