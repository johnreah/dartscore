import os
import unittest
from pathlib import Path

from preferences import Preferences

PREFS_TEST_FILE_NAME = "dartscore-test.ini"

class PreferencesTest(unittest.TestCase):

    def test_whenNoFileExists_thenDefaultValuesAreUsed(self):
        path = Path(os.path.join(Path().home(), PREFS_TEST_FILE_NAME))
        if path.exists():
            path.unlink()
        preferences = Preferences(PREFS_TEST_FILE_NAME)
        self.assertTrue(preferences.sound_button_clicks)
        self.assertTrue(preferences.tts_say_score_required)
        self.assertTrue(preferences.tts_say_totals)
        self.assertEqual(preferences.tts_voice, "en_GB-alba-medium")

    def test_whenValueChanged_theItStaysChanged(self):
        preferences = Preferences(Path(os.path.join(Path().home(), PREFS_TEST_FILE_NAME)))
        preferences.sound_button_clicks = False
        self.assertFalse(preferences.sound_button_clicks)

    def tearDown(self):
        path = Path(os.path.join(Path().home(), PREFS_TEST_FILE_NAME))
        if path.exists():
            path.unlink()
