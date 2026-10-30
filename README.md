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

## Installation on Windows (numbered, tested order)

1. Download the repo ZIP from GitHub and extract it.
2. Open the **inner** folder in VS Code / PowerShell — the prompt must
   read `PS D:\expermental zone\creox-air-control-main\creox-air-control-main>`
   (the project root). Running from the outer folder or from inside
   `creox_gesture/` gives "module not found" — this tripped us before.
3. Install backend dependencies:
```powershell
python -m pip install -r requirements.txt
```
4. Download `hand_landmarker.task` from
   https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
   and put it in the `creox_gesture/` folder. **Re-place it after every
   fresh ZIP download** — it is NOT in the ZIP (binary file).
5. Run the app:
```powershell
python -m creox_gesture.app
```
   Or pick a profile directly: `python -m creox_gesture.app --profile suit`
6. Press `G` to toggle gesture mode ON (it starts OFF on purpose),
   `P` to cycle profiles, `Q` to quit. The preview window always shows
   mode + profile + detected gesture.
7. For the Suit HUD: open `suit_hud.html` in a browser and focus it
   first, then run with `--profile suit` (or press `P` until it says
   `suit`). All HUD systems are SIMULATED.

Optional calibration: copy the values in `air_control_settings.json`
and edit them (pinch threshold, debounce, swipe). Bad values fall back
to safe defaults — the app never crashes on bad settings.

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
- `tests/test_profiles.py` — profile tests (incl. no Aegis profile)
- `tests/test_legendary.py` — 9 legendary cases (ClickGate, settings, profiles, history)
- Total: **22 tests, all passing** (no camera needed)
- `BLUEPRINT.md` — the locked blueprint

## Phase 2 — Suit HUD (standalone, NOT an Aegis project)
Open `suit_hud.html` in a browser, focus it, then run the app with
`--profile suit` (or press `P` in the preview window to switch profiles).
Gestures: move = cursor, pinch = toggle the focused system, swipe
right/left = Tab / Shift+Tab (next/previous system), hand up/down =
scroll the log, open palm = pause. All Suit HUD systems (POWER CORE,
HELMET, REPULSOR, FLIGHT) are SIMULATED — this is a control-panel
prototype for a future suit design, not a real suit.

## Legendary package (2026-10-30)
See `LEGENDARY.md` — v1.1 one-pinch-one-click, calibration settings,
gesture history log, browser + media profiles, Suit HUD v2 with a
gesture legend, architecture diagram (`docs/architecture.svg`), and
numbered Windows installation. Tests: 22/22 pass (no camera needed).
Laptop test of Phase 2 + Legendary is still pending on Akash's laptop.

## Later phases (roadmap only, not built)
Phone control, ESP32 wristband version — see
`docs/phone-esp32-roadmap.md`. No prices checked, no code claimed.
