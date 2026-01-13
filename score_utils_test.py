import unittest

import score_utils

class ScoreUtilsTest(unittest.TestCase):
    def test_below_zero(self):
        self.assertFalse(score_utils.is_valid_score(-1), "Negative score should be invalid")

    def test_above_180(self):
        self.assertFalse(score_utils.is_valid_score(181), "Score >180 should be invalid")

    def test_impossible_score(self):
        impossible_score = 179
        self.assertFalse(score_utils.is_valid_score(impossible_score), "Score {} cannot be made with 3 darts".format(impossible_score))

    def test_valid_score(self):
        valid_score = 177
        self.assertTrue(score_utils.is_valid_score(valid_score), "Score {} should be valid".format(valid_score))

    def test_suggested_checkouts(self):
        score = 9
        expected_checkouts = 2
        suggested_checkouts = score_utils.suggested_checkouts(score)
        self.assertEqual(len(suggested_checkouts), expected_checkouts, "Number of suggested checkouts for score {} should be {}".format(score, expected_checkouts))

        score = 180
        expected_checkouts = 0
        suggested_checkouts = score_utils.suggested_checkouts(score)
        self.assertEqual(len(suggested_checkouts), expected_checkouts, "Number of suggested checkouts for score {} should be {}".format(score, expected_checkouts))

        score = 64
        expected_checkouts = 3
        suggested_checkouts = score_utils.suggested_checkouts(score)
        self.assertEqual(len(suggested_checkouts), expected_checkouts, "Number of suggested checkouts for score {} should be {}".format(score, expected_checkouts))

    def test_checkout_exists_when_exists(self):
        score = 170
        self.assertTrue(score_utils.checkout_exists(score), "There should be a checkout for {}".format(score))

    def test_checkout_exists_when_not_exists(self):
        score = 179
        self.assertFalse(score_utils.checkout_exists(score), "No checkout should exist for {}".format(score))


if __name__ == '__main__':
    unittest.main()
