from finance_utils import *
import unittest

class FinanceUtilsGradingTests(unittest.TestCase):
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

    # get_even_redistribution Tests
    # -------------------------------------------------
    def test_get_even_redistribution_t0(self) -> None:
        self.assertEqual([2, 2, 2], get_even_redistribution([3, 2, 1]))
        self.assertEqual([2, 2, 2], get_even_redistribution([2, 2, 2]))
        self.assertEqual([2, 2, 2], get_even_redistribution([1, 2, 3]))

    def test_get_even_redistribution_t1(self) -> None:
        self.assertEqual([2, 2, 2, 3], get_even_redistribution([3, 2, 1, 3]))
        self.assertEqual([2, 2, 3, 3], get_even_redistribution([3, 2, 2, 3]))
        self.assertEqual([2, 3, 3, 3], get_even_redistribution([4, 2, 2, 3]))
        self.assertEqual([3, 3, 3, 3], get_even_redistribution([4, 3, 2, 3]))

    # Possible edge cases
    def test_get_even_redistribution_t2(self) -> None:
        # Empty list
        self.assertEqual([], get_even_redistribution([])) 
        # List with one element
        self.assertEqual([1], get_even_redistribution([1]))
        # List with negative values
        self.assertRaises(ValueError, get_even_redistribution, ([1, -2, 3]))
        # List that is already even
        self.assertEqual([2, 2, 2, 2], get_even_redistribution([2, 2, 2, 2]))

    # greedy_changemaker tests
    # -------------------------------------------------

    def test_greedy_changemaker_t0(self) -> None:
        self.assertEqual([1, 0, 0, 0], greedy_changemaker(1))
        self.assertEqual([0, 1, 0, 0], greedy_changemaker(5))
        self.assertEqual([0, 0, 1, 0], greedy_changemaker(10))
        self.assertEqual([0, 0, 0, 1], greedy_changemaker(25))

    def test_greedy_changemaker_t1(self) -> None:
        self.assertEqual([3, 0, 0, 0], greedy_changemaker(3))
        self.assertEqual([0, 0, 2, 0], greedy_changemaker(20))

    # Possible edge cases
    def test_greedy_changemaker_t2(self) -> None:
        # Test amount zero
        self.assertEqual([0, 0, 0, 0], greedy_changemaker(0))
        # Test negative amount
        self.assertRaises(ValueError, greedy_changemaker, (-1))
        # Test for type
        self.assertRaises(TypeError, greedy_changemaker, (12.5))

if __name__ == '__main__':
    unittest.main()