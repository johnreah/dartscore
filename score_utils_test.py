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

if __name__ == '__main__':
    unittest.main()
