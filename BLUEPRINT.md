# Creox Air Control — Camera Blueprint (LOCKED 2026-10-30, build started)

**Project/repo name LOCKED 2026-10-30: creox-air-control.**

## Locked decisions (Akash's own picks)
1. **Route:** Laptop webcam camera route (MediaPipe-style hand tracking) — 2026-10-30
2. **Form:** Standalone project, NOT an Aegis Prime module — 2026-10-30
3. **First control target:** Laptop slides + music — 2026-10-30
4. **Watch role:** Noise watch stays for calls/music/notifications only — it is NOT the gesture controller (closed system, no open SDK)

## Project (working title, name NOT decided yet)
Camera Gesture Control — standalone, local-only, own laptop only.
Name to be chosen by Akash before repo creation; do not invent a brand name as decided.

## Stack (Phase 1, laptop-testable with existing tools)
- Python (his laptop already has Python 3.14)
- OpenCV for webcam capture + MediaPipe Hands (21 hand landmarks)
- Action dispatcher via OS key events only (pyautogui / keyboard-style media keys)
- No network, no cloud, no other device control in Phase 1

## Gesture set (only 6, Phase 1)
| Gesture | Action (slides + music only) |
|---|---|
| Index finger move | Move cursor / highlight slide area |
| Pinch (thumb + index together) | Click / select |
| Swipe / tilt left | Previous slide / previous song |
| Swipe / tilt right | Next slide / next song |
| Tilt up | Volume up |
| Tilt down | Volume down |
| Open palm hold | PAUSE gestures (safety stop, while held) |

## Mode + safety (non-negotiable)
- Gesture mode is explicitly ON/OFF: toggle with the `G` key or an on-screen button. Never always-on.
- On-screen mode indicator must always be visible (ON = green, OFF/paused = red).
- Debounce: same gesture must hold ~300 ms before firing, so a passing hand does not trigger actions.
- Hand lost / low light: no action at all, show a warning — never guess a gesture.
- Allowlist only: the actions in the table above. NO file delete, NO system settings change, NO other-device control in Phase 1.
- Control is only for his own laptop, his own slides and his own music.

## Architecture (Phase 1)
Webcam → MediaPipe Hands landmarks → Gesture classifier (landmark distances + angles, debounced)
→ Action dispatcher (allowlisted key events only) → Slides app / music player
A small preview window shows the camera feed + detected gesture + mode, so he can see what the system sees.

## Test plan (his laptop only, guide-only)
1. Camera opens, hand detected, mode indicator visible.
2. Each of the 6 gestures fires its table action once (not repeatedly).
3. Open palm hold pauses everything; mode OFF stops everything.
4. Low light / hand out of frame: no stray actions.
Muse prepares instructions/files; Akash runs and verifies on his laptop.

## Later phases (NOT Phase 1, do not start unprompted)
- Phase 2: Aegis HUD control (only if he asks)
- Phase 3: Phone control
- Phase 4: ESP32 + MPU6050 wristband version (same gesture set, hardware needed, prices to check first)

## Open (his answers only)
- Project name + repo name
- Whether this counts toward his 185-project target (likely yes as a standalone project, but his call)
- Slide app to test first (PowerPoint / Google Slides / PDF viewer — his pick)
