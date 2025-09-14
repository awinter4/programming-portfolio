from ternary_tree_text_filler import TernaryTreeTextFiller
import unittest


class TextFillerGradingTests(unittest.TestCase):
    # =================================================
    # Test Configuration
    # =================================================

    # Used as the basic empty TextFiller to test
    # the setUp() method is run before every test
    def setUp(self) -> None:
        self.tf = TernaryTreeTextFiller()

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

    # Initialization tests
    # -------------------------------------------------
    def test_autocompleter(self) -> None:
        self.assertTrue(self.tf.is_empty())

    # Basic tests
    # -------------------------------------------------
    def test_add_t0(self) -> None:
        self.tf.add('is')
        self.tf.add('it')
        self.tf.add('as')
        self.tf.add('ass')
        self.tf.add('at')
        self.tf.add('bat')

    def test_size_t0(self) -> None:
        self.tf.add('is')
        self.tf.add('it')
        self.tf.add('as')
        self.assertEqual(3, len(self.tf))
        self.tf.add('as')
        self.assertEqual(3, len(self.tf))

    def test_contains_t0(self) -> None:
        self.tf.add('is')
        self.tf.add('it')
        self.tf.add('as')
        self.tf.add('ass')
        self.tf.add('at')
        self.tf.add('bat')

        self.assertTrue(self.tf.contains('is'))
        self.assertTrue(self.tf.contains('it'))
        self.assertTrue(self.tf.contains('as'))
        self.assertTrue(self.tf.contains('ass'))
        self.assertTrue(self.tf.contains('at'))
        self.assertTrue(self.tf.contains('bat'))

        self.assertFalse(self.tf.contains('ii'))
        self.assertFalse(self.tf.contains('i'))
        self.assertFalse(self.tf.contains('zoo'))

    def test_text_fill_t0(self) -> None:
        self.tf.add('is')
        self.tf.add('it')
        self.tf.add('as')
        self.tf.add('at')
        self.tf.add('item')
        self.tf.add('ass')
        self.tf.add('bat')
        self.tf.add('bother')
        self.tf.add('goat')
        self.tf.add('goad')

        self.assertEqual('is', self.tf.text_fill('is'))
        self.assertEqual('item', self.tf.text_fill('ite'))
        self.assertEqual('bat', self.tf.text_fill('ba'))
        self.assertEqual('bother', self.tf.text_fill('bo'))

        self.assertIsNone(self.tf.text_fill('bad'))
        self.assertIsNone(self.tf.text_fill('zoo'))

        self.assertTrue((s := self.tf.text_fill('it')) == 'it' or s == 'item')
        self.assertTrue((s := self.tf.text_fill('go')) == 'goat' or s == 'goad')
        self.assertTrue((s := self.tf.text_fill('as')) == 'as' or s == 'ass')

    def test_get_sorted_list_t0(self) -> None:
        self.tf.add('is')
        self.tf.add('it')
        self.tf.add('as')
        self.tf.add('itinerary')
        self.tf.add('ass')
        self.tf.add('at')
        self.tf.add('zoo')
        self.tf.add('bat')
        self.tf.add('bother')

        self.assertListEqual(
            ['as', 'ass', 'at', 'bat', 'bother', 'is', 'it', 'itinerary', 'zoo'],
            self.tf.get_sorted_list(),
        )

if __name__ == "__main__":
    unittest.main()