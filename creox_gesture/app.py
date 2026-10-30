"""Webcam app — Creox Air Control, Legendary package.

Run from the project folder on his laptop:
    python -m pip install -r requirements.txt
    python -m creox_gesture.app

MediaPipe 1.x removed the old mp.solutions API, so this app uses the
new Tasks API (HandLandmarker). That needs one model file, which is
NOT in the repo (binary files cannot be pushed by the Muse app):
    1. Download hand_landmarker.task from
       https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
    2. Put it in the creox_gesture/ folder, next to this file.
    3. Run the app again. If the file is missing, the app says so
       plainly instead of crashing. Re-place it after every fresh
       ZIP download — it is not in the ZIP.

Controls: G toggles gesture mode ON/OFF, P cycles profiles
(slides_music -> suit -> browser -> media), Q quits. Mode starts OFF.
Legendary changes: one pinch = one click (ClickGate, no more repeat
clicks while held); settings from air_control_settings.json
(calibration, never crashes on bad settings); every fired action is
logged to gesture_log.jsonl for debugging.

Profiles: slides_music (Phase 1, laptop-verified), suit (Phase 2,
Suit HUD — all systems SIMULATED), browser (tabs), media (tracks).
Air Control stays standalone and is NOT an Aegis project: it only
sends generic key/click/scroll actions to the active window.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from .actions import fire
from .gestures import ClickGate, SwipeDetector, classify
from .history import GestureHistory
from .profiles import PROFILES, translate
from .settings import Settings

MODEL_NAME = "hand_landmarker.task"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="slides_music",
                        choices=list(PROFILES))
    parser.add_argument("--settings", default=None,
                        help="Path to air_control_settings.json (optional)")
    args = parser.parse_args()
    profile = args.profile
    settings = Settings.load(args.settings)
    print(f"Settings: {settings.source} "
          f"(debounce={settings.debounce_seconds}s, "
          f"pinch={settings.pinch_threshold}, swipe={settings.swipe_threshold})")
    try:
        import cv2
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision
    except ImportError as exc:
        print(f"Missing package: {exc.name}. Run: python -m pip install -r requirements.txt")
        return 1
    model_path = Path(__file__).parent / MODEL_NAME
    if not model_path.exists():
        print(f"Model file missing: {model_path}")
        print("Download hand_landmarker.task from:")
        print("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        print(f"Then put it in: {model_path.parent}")
        return 1
    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(model_path)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=settings.min_hand_detection_confidence,
        min_tracking_confidence=settings.min_tracking_confidence,
    )
    mode_on = False
    last_fired = 0.0
    swipe = SwipeDetector(window=settings.swipe_window,
                          threshold=settings.swipe_threshold,
                          cooldown_frames=settings.swipe_cooldown_frames)
    click_gate = ClickGate()
    history = GestureHistory(max_events=settings.gesture_log_max_events,
                             log_file=settings.gesture_log_file)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not found. Plug in / enable the laptop camera and retry.")
        return 1
    print(f"Profile: {profile}. Gesture mode starts OFF. Press G to toggle, P for profile, Q to quit.")
    with vision.HandLandmarker.create_from_options(options) as landmarker:
        frame_no = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            frame_no += 1
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result = landmarker.detect_for_video(
                mp_image, timestamp_ms=frame_no * 33)
            gesture = None
            if result.hand_landmarks:
                lm = [(p.x, p.y) for p in result.hand_landmarks[0]]
                gesture = classify(lm, pinch_threshold=settings.pinch_threshold)
                swipe_result = swipe.update(lm[8])
                if gesture != "palm_pause" and swipe_result:
                    gesture = swipe_result
            now = time.time()
            if (mode_on and gesture and gesture != "palm_pause"
                    and click_gate.allow(gesture)
                    and now - last_fired >= settings.debounce_seconds):
                action = translate(profile, gesture)
                description, performed = fire(action) if action else (None, False)
                if description:
                    print(f"{profile} | {gesture} -> {action}: {description}")
                    history.record(gesture, action, performed)
                last_fired = now
            label = f"MODE: {'ON' if mode_on else 'OFF'}  {profile}  GESTURE: {gesture or '-'}"
            cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0) if mode_on else (0, 0, 255), 2)
            cv2.imshow("Creox Air Control (G = mode, P = profile, Q = quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("g"), ord("G")):
                mode_on = not mode_on
                print(f"Gesture mode {'ON' if mode_on else 'OFF'}")
            elif key in (ord("p"), ord("P")):
                names = list(PROFILES)
                profile = names[(names.index(profile) + 1) % len(names)]
                print(f"Profile: {profile}")
            elif key in (ord("q"), ord("Q")):
                break
    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
