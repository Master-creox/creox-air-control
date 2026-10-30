import json
import unittest
from pathlib import Path

from creox_gesture.gestures import ClickGate
from creox_gesture.history import GestureHistory
from creox_gesture.profiles import PROFILES, translate
from creox_gesture.settings import Settings


class TestClickGate(unittest.TestCase):
    def test_one_pinch_one_click(self):
        gate = ClickGate()
        self.assertTrue(gate.allow("click"))
        self.assertFalse(gate.allow("click"))  # held pinch: silent
        self.assertFalse(gate.allow("click"))
        self.assertTrue(gate.allow("move"))  # release / other gesture
        self.assertTrue(gate.allow("click"))  # fresh pinch fires again

    def test_other_gestures_always_allowed(self):
        gate = ClickGate()
        for gesture in ("move", "next", "prev", "volume_up", "palm_pause"):
            self.assertTrue(gate.allow(gesture))


class TestSettings(unittest.TestCase):
    def test_defaults_when_no_file(self):
        settings = Settings.load("/tmp/does-not-exist-air-control.json")
        self.assertEqual(settings.debounce_seconds, 0.3)
        self.assertEqual(settings.pinch_threshold, 0.05)

    def test_bad_json_and_bad_values_fall_back(self):
        bad = Path("/tmp/air-bad-settings.json")
        bad.write_text("{not json", encoding="utf-8")
        self.assertEqual(Settings.load(bad).pinch_threshold, 0.05)
        out_of_range = Path("/tmp/air-range-settings.json")
        out_of_range.write_text(json.dumps({"pinch_threshold": 99.0,
                                            "debounce_seconds": 0.2}),
                                encoding="utf-8")
        loaded = Settings.load(out_of_range)
        self.assertEqual(loaded.pinch_threshold, 0.05)  # rejected
        self.assertEqual(loaded.debounce_seconds, 0.2)  # accepted

    def test_good_file_loads(self):
        good = Path("/tmp/air-good-settings.json")
        good.write_text(json.dumps({"pinch_threshold": 0.08,
                                    "unknown_key": 123}),
                        encoding="utf-8")
        self.assertEqual(Settings.load(good).pinch_threshold, 0.08)


class TestProfiles(unittest.TestCase):
    def test_browser_and_media_profiles(self):
        self.assertEqual(translate("browser", "next"), "next_tab")
        self.assertEqual(translate("browser", "prev"), "prev_tab")
        self.assertEqual(translate("media", "next"), "media_next")
        self.assertEqual(translate("media", "click"), "media_play_pause")
        self.assertEqual(translate("suit", "next"), "panel_next")
        self.assertEqual(translate("slides_music", "next"), "next")

    def test_no_aegis_profile(self):
        self.assertNotIn("aegis", PROFILES)

    def test_every_profile_covers_all_gestures(self):
        gestures = ("move", "click", "next", "prev",
                    "volume_up", "volume_down", "palm_pause")
        for name, mapping in PROFILES.items():
            for gesture in gestures:
                self.assertIn(gesture, mapping, f"{name} missing {gesture}")


class TestHistory(unittest.TestCase):
    def test_ring_buffer_and_last(self):
        history = GestureHistory(max_events=3)
        for i in range(5):
            history.record("click", "click", True)
        self.assertEqual(len(history.events), 3)
        self.assertEqual(len(history.last(2)), 2)


if __name__ == "__main__":
    unittest.main()
