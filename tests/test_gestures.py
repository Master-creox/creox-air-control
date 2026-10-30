import unittest

from creox_gesture.actions import ACTIONS, describe
from creox_gesture.gestures import SwipeDetector, classify


def make_hand(extended, pinch=False):
    """Build 21 synthetic landmarks: extended fingers point up (y small),
    folded fingers point down near the palm (y large)."""
    lm = [(0.5, 0.9)] * 21
    lm = list(lm)
    lm[0] = (0.5, 0.9)  # wrist
    tips = {"index": 8, "middle": 12, "ring": 16, "pinky": 20}
    pips = {"index": 6, "middle": 10, "ring": 14, "pinky": 18}
    for finger, tip in tips.items():
        pip = pips[finger]
        lm[pip] = (0.5, 0.5)
        lm[tip] = (0.5, 0.2) if finger in extended else (0.5, 0.7)
    lm[4] = (0.48, 0.22) if pinch else (0.3, 0.5)  # thumb tip
    return lm


class TestClassify(unittest.TestCase):
    def test_open_palm_pauses(self):
        hand = make_hand({"index", "middle", "ring", "pinky"})
        self.assertEqual(classify(hand), "palm_pause")

    def test_index_only_moves(self):
        hand = make_hand({"index"})
        self.assertEqual(classify(hand), "move")

    def test_pinch_clicks(self):
        hand = make_hand({"index"}, pinch=True)
        self.assertEqual(classify(hand), "click")

    def test_fist_does_nothing(self):
        hand = make_hand(set())
        self.assertIsNone(classify(hand))

    def test_unclear_hand_does_nothing(self):
        self.assertIsNone(classify(None))
        self.assertIsNone(classify([(0, 0)] * 10))

    def test_swipe_right_is_next(self):
        detector = SwipeDetector(window=4, threshold=0.25, cooldown_frames=2)
        result = None
        for x in (0.2, 0.3, 0.4, 0.55):
            result = detector.update((x, 0.5))
        self.assertEqual(result, "next")

    def test_swipe_left_is_prev(self):
        detector = SwipeDetector(window=4, threshold=0.25, cooldown_frames=2)
        result = None
        for x in (0.6, 0.5, 0.4, 0.3):
            result = detector.update((x, 0.5))
        self.assertEqual(result, "prev")

    def test_small_movement_is_not_a_swipe(self):
        detector = SwipeDetector(window=4, threshold=0.25, cooldown_frames=2)
        result = None
        for x in (0.4, 0.42, 0.44, 0.45):
            result = detector.update((x, 0.5))
        self.assertIsNone(result)

    def test_action_allowlist_covers_all_gestures(self):
        for gesture in ("move", "click", "next", "prev",
                        "volume_up", "volume_down", "palm_pause"):
            self.assertIn(gesture, ACTIONS)
            self.assertIsNotNone(describe(gesture))


if __name__ == "__main__":
    unittest.main()
