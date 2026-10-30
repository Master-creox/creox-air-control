# Phone + ESP32 wristband — ROADMAP ONLY (not built, not tested)

This is the Legendary package's honest future plan. Nothing in this
document is implemented code, and nothing here should be claimed as
working until it is built and tested on real hardware.

## Phone control (future)
- Idea: phone as a second gesture surface / remote for the laptop app.
- Open questions (Akash decides): phone app vs web page, Bluetooth vs
  Wi-Fi on the same network, and what the phone is allowed to control.
- Rule carried over: explicit ON/OFF, allowlist only, own devices only.

## ESP32 + MPU6050 wristband (future)
- Idea: wrist-worn sensor sends motion data; laptop app translates it
  into the same gesture -> action pipeline (same profiles, same gates).
- Open questions: ESP32 board choice, MPU6050 wiring, wireless link
  (BLE vs Wi-Fi), battery, and cost — prices were NOT checked yet.
- Rule carried over: sensor data is motion only; no camera, no audio.

## What would make these "done"
1. Working prototype on Akash's own hardware.
2. Tests that do not need the hardware (same pattern as gestures.py).
3. Tested installation instructions, like the Windows section in README.
4. A clear statement of what is simulated vs real — never faked live data.
