import unittest

from creox_gesture.actions import ACTIONS
from creox_gesture.profiles import PROFILES, translate


class TestProfiles(unittest.TestCase):
    def test_slides_profile_unchanged(self):
        self.assertEqual(translate("slides_music", "next"), "next")
        self.assertEqual(translate("slides_music", "volume_up"), "volume_up")

    def test_suit_profile_has_chat_and_navigation_together(self):
        # Chat-style log scroll + system navigation, both in one profile.
        self.assertEqual(translate("suit", "volume_up"), "scroll_up")
        self.assertEqual(translate("suit", "volume_down"), "scroll_down")
        self.assertEqual(translate("suit", "next"), "panel_next")
        self.assertEqual(translate("suit", "prev"), "panel_prev")
        self.assertEqual(translate("suit", "click"), "click")

    def test_no_aegis_profile(self):
        # Air Control is NOT an Aegis project (user correction 2026-10-30).
        self.assertNotIn("aegis", PROFILES)

    def test_every_mapped_action_exists(self):
        for profile in PROFILES.values():
            for action in profile.values():
                self.assertIn(action, ACTIONS)


if __name__ == "__main__":
    unittest.main()
