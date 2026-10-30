"""Webcam app — Phase 1: slides + music, own laptop only.

Run from the project folder on his laptop:
    python -m pip install -r requirements.txt
    python -m creox_gesture.app

Controls: press G to toggle gesture mode ON/OFF, Q to quit.
The preview window always shows mode + detected gesture, so the user
sees exactly what the system sees. Mode starts OFF on purpose.
If OpenCV / MediaPipe are missing, the app says so plainly instead
of crashing with a traceback.
"""
from __future__ import annotations

import time

from .actions import describe, fire
from .gestures import SwipeDetector, classify


def main():
    try:
        import cv2
        import mediapipe as mp
    except ImportError as exc:
        print(f"Missing package: {exc.name}. Run: python -m pip install -r requirements.txt")
        return 1
    mode_on = False
    last_fired = 0.0
    swipe = SwipeDetector()
    hands = mp.solutions.hands.Hands(
        max_num_hands=1, min_detection_confidence=0.7,
        min_tracking_confidence=0.7)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not found. Plug in / enable the laptop camera and retry.")
        return 1
    print("Gesture mode starts OFF. Press G to toggle, Q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        gesture = None
        if result.multi_hand_landmarks:
            lm = [(p.x, p.y) for p in result.multi_hand_landmarks[0].landmark]
            gesture = classify(lm)
            swipe_result = swipe.update(lm[8])
            if gesture == "palm_pause":
                gesture = "palm_pause"
            elif swipe_result:
                gesture = swipe_result
        now = time.time()
        if mode_on and gesture and gesture != "palm_pause" and now - last_fired >= 0.3:
            description, _performed = fire(gesture)
            if description:
                print(f"{gesture}: {description}")
            last_fired = now
        label = f"MODE: {'ON' if mode_on else 'OFF'}  GESTURE: {gesture or '-'}"
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0) if mode_on else (0, 0, 255), 2)
        cv2.imshow("Creox Gesture Control (G = mode, Q = quit)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("g"), ord("G")):
            mode_on = not mode_on
            print(f"Gesture mode {'ON' if mode_on else 'OFF'}")
        elif key in (ord("q"), ord("Q")):
            break
    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
