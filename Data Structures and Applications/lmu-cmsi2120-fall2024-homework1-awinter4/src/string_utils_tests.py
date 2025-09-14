from string_utils import *
import unittest

class StringUtilsGradingTests(unittest.TestCase):
    # =================================================
    # Unit Tests
    # =================================================
    # For grading purposes, every method and unit is 
    # weighted equally and totaled for the score.
    # The tests increase in difficulty such that the
    # basics are unlabeled and harder tiers are tagged
    # t0, t1, t2, t3, ... easier -> harder
    #
    # Typically, you cluster tests for each method
    # by particular types of inputs, e.g., empty String
    # inputs vs. single words vs. multiple words (the
    # "zero-one-infinity" rule of testing) or tests for
    # proper error handling. Some of the below may be
    # organized for grading purposes instead.

    # has_sequence Tests
    # -------------------------------------------------

    def test_has_sequence_t0(self) -> None:
        self.assertTrue(has_sequence('GGGG', 'GG'))
        self.assertTrue(has_sequence('GTGTGTG', 'GG'))

    def test_has_sequence_t1(self) -> None:
        self.assertFalse(has_sequence('GTC', 'CGT'))
        self.assertFalse(has_sequence('TTT', 'TTTT'))

    def test_has_sequence_t2(self) -> None:
        self.assertTrue(has_sequence('CCCC', 'CC'))
        self.assertTrue(has_sequence('CGATTAGC', 'CATTC'))

    # Possible edge cases
    def test_has_sequence_t3(self) -> None:
        # Test empty corpus and query
        self.assertFalse(has_sequence('', 'ABC'))
        self.assertTrue(has_sequence('ABC', ''))
        self.assertTrue(has_sequence('', ''))
        # Test case sensitivity
        self.assertFalse(has_sequence('ABC', 'abc'))
        self.assertFalse(has_sequence('abc', 'ABC'))
        self.assertTrue(has_sequence('AbCdEfG', 'ACEG'))
        # Test repeated characters
        self.assertTrue(has_sequence('AABBCCDDEEFF', 'AABDDE'))

    # capitalize_sentence tests
    # -------------------------------------------------

    def test_capitalize_sentence_t0(self) -> None:
        self.assertEqual('Yo.', capitalize_sentence('Yo.'))

    def test_capitalize_sentence_t1(self) -> None:
        self.assertEqual(
            'Hello. My name is Java.', capitalize_sentence('Hello. my name is Java.')
        )

    def test_capitalize_sentence_t2(self) -> None:
        self.assertEqual(
            'I.   Like.    Spaces.', capitalize_sentence('I.   like.    spaces.')
        )

    # Possible edge cases
    def test_capitalize_sentence_t3(self) -> None:
        # Test empty str
        self.assertEqual('', capitalize_sentence(''))
        # Test str with no periods
        self.assertEqual('Andrew', capitalize_sentence('andrew'))
        # Test str with multiple periods
        self.assertEqual('Andrew. . . Andrew', capitalize_sentence('andrew. . . andrew'))

    # get_nth_match tests
    # -------------------------------------------------

    def test_get_nth_match_t0(self) -> None:
        self.assertEqual('test', get_nth_match('test test test', 'test', 0))
        self.assertEqual('test', get_nth_match('test test test', 'test', 1))
        self.assertEqual('test', get_nth_match('test test test', 'test', 2))
        self.assertEqual('', get_nth_match('test test test', 'test', 3))

    def test_get_nth_match_t1(self) -> None:
        self.assertEqual('test', get_nth_match('test Test tEsT', 'test', 0))
        self.assertEqual('Test', get_nth_match('test Test tEsT', 'test', 1))
        self.assertEqual('tEsT', get_nth_match('test Test tEsT', 'test', 2))
        self.assertEqual('', get_nth_match('test Test tEsT', 'test', 3))

    def test_get_nth_match_t2(self) -> None:
        self.assertEqual('', get_nth_match('test Test tEsT', 'notest', 1))

    # Possible edge cases
    def test_get_nth_match_t3(self) -> None:
        # Test input validation
        self.assertRaises(ValueError, get_nth_match, 'test test', 'test', -1)
        # Test when n is larger than n matches
        self.assertEqual('', get_nth_match('test test', 'test', 3))
        # Test when query matches part of a word
        self.assertEqual('', get_nth_match('testing teststring tests', 'test', 0))

if __name__ == '__main__':
    unittest.main()