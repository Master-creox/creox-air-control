# Creox Air Control — Legendary Package

TraceLab-style legendary: milestones, tests, tested installation,
diagram — not just more features. Built 2026-10-30, on top of the
laptop-verified Phase 1 and the pushed Phase 2 Suit HUD.

## What is legendary here

### L1 — Polish (v1.1)
- **One pinch = one click** (ClickGate): a held pinch no longer
  re-fires every 300 ms. Release and pinch again to click again.
- **Calibration settings** (`air_control_settings.json`): debounce,
  pinch threshold, swipe threshold/window/cooldown, detection
  confidences, log file and size. Bad JSON, unknown keys, or
  out-of-range values fall back to safe defaults — never a crash.
- **Gesture history** (`gesture_log.jsonl`, local only): every fired
  action with time, gesture, action, and whether it really performed.
  If a gesture misfires, the log shows what the app actually did.

### L2 — New profiles (same 6 gestures)
- **browser**: swipe = next/prev tab (Ctrl+Tab / Ctrl+Shift+Tab),
  hand up/down = scroll page, pinch = click.
- **media**: swipe = next/prev track, pinch = play/pause,
  hand up/down = volume. Press `P` to cycle all 4 profiles.

### L3 — Suit HUD v2
- Gesture legend table for all 4 profiles added to `suit_hud.html`.
- HUD script re-checked with `node --check` (passed).
- The 4 systems stay **SIMULATED** and labelled as such — no fake
  live data was added.

### L4 — Diagram + tested installation
- `docs/architecture.svg`: webcam -> MediaPipe -> classifier ->
  gates -> profiles -> allowlisted actions -> active window.
- README now has numbered Windows installation instructions
  (extract ZIP, inner folder, venv, pip, model file, run, keys).
  Tested on this VM: unit tests 22/22, app syntax, settings JSON,
  HUD JS — see "Tested" below.

### L5 — Honest limits (still true)
- **Laptop test of Phase 2 + Legendary is still pending** on Akash's
  laptop — this package is code-complete, not laptop-verified yet.
- **Phone control and ESP32 wristband are NOT built** — only a
  roadmap document (`docs/phone-esp32-roadmap.md`), no prices checked.
- The MediaPipe `.task` model file is NOT in the repo (binary) and
  must be re-placed after every fresh ZIP download.
- Suit HUD systems are simulated, not a real suit.

## Tested (2026-10-30, VM, no camera)
- `python -m unittest discover -s tests -t .` — **22/22 pass**
  (was 13; +9 legendary: ClickGate, settings, profiles, history).
- `node --check` on the HUD script — passed.
- Settings example JSON parses; bad settings fall back to defaults.
- App `--help` / missing-model path: the app prints a plain message
  instead of crashing (same behaviour as Phase 1).

## Not tested yet (needs Akash's laptop)
- Webcam run with the real `.task` model, all 4 profiles, Suit HUD
  focus + Tab navigation, browser tabs, media keys, and the
  one-pinch-one-click feel in real use.
