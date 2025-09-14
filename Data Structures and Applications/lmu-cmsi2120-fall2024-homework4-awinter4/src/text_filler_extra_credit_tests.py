from ternary_tree_text_filler import TernaryTreeTextFiller
import unittest


class TextFillerGradingExtraCreditTests(unittest.TestCase):
    # =================================================
    # Test Configuration
    # =================================================

    # Used as the basic empty TextFiller to test
    # the setUp() method is run before every test
    def setUp(self) -> None:
        self.tf = TernaryTreeTextFiller()

    # =================================================
    # Unit Tests
    # [!] NOTE: These are all tests for the extra credit
    # portion of this assignment; to receive full credit
    # on the base assignment, you *do not* need to pass
    # any of the following:
    # =================================================

    def test_add_priority_term_t0(self) -> None:
        self.tf.add('is', 2)
        self.tf.add('it', 3)
        self.tf.add('as', 3)
        self.tf.add('ass', 4)
        self.tf.add('at', 2)
        self.tf.add('bat', 1)
    
    def test_text_fill_premium_t0(self) -> None:
        self.tf.add('is', 2)
        self.tf.add('it', 3)
        self.tf.add('as', 3)
        self.tf.add('ass', 4)
        self.tf.add('at', 2)
        self.tf.add('bat', 1)

        self.assertIsNone(self.tf.text_fill_premium('z'))
        self.assertIsNone(self.tf.text_fill_premium('zap'))

        self.assertEqual('it', self.tf.text_fill_premium('i'))
        self.assertEqual('is', self.tf.text_fill_premium('is'))
        self.assertEqual('ass', self.tf.text_fill_premium('a'))
        self.assertEqual('ass', self.tf.text_fill_premium('as'))
        self.assertEqual('ass', self.tf.text_fill_premium('ass'))
        self.assertEqual('at', self.tf.text_fill_premium('at'))
        self.assertEqual('bat', self.tf.text_fill_premium('b'))
    
    def test_text_fill_premium_t1(self) -> None:
        self.tf.add('is', 2)
        self.tf.add('it', 3)
        self.tf.add('as', 3)
        self.tf.add('ass', 4)
        self.tf.add('at', 2)
        self.tf.add('bat', 1)
        self.tf.add('batch', 3)
        self.tf.add('irk', 5)
        self.tf.add('art', 5)
        self.tf.add('asp', 3)

        self.assertEqual('batch', self.tf.text_fill_premium('bat'))
        self.assertEqual('irk', self.tf.text_fill_premium('i'))
        self.assertEqual('art', self.tf.text_fill_premium('a'))
        self.assertEqual('ass', self.tf.text_fill_premium('as'))
    
    def test_text_fill_premium_t2(self) -> None:
        self.tf.add('a', 1)
        self.tf.add('ab', 2)
        self.tf.add('abate', 3)
        self.tf.add('act', 4)
        self.tf.add('activate', 5)
        self.tf.add('active', 4)

        self.assertEqual('activate', self.tf.text_fill_premium('a'))
        self.assertEqual('activate', self.tf.text_fill_premium('act'))
        self.assertEqual('activate', self.tf.text_fill_premium('acti'))
        self.assertEqual('active', self.tf.text_fill_premium('active'))
        self.assertEqual('abate', self.tf.text_fill_premium('ab'))
        self.assertEqual('abate', self.tf.text_fill_premium('aba'))

        self.assertIsNone(self.tf.text_fill_premium('activae'))
    
    def test_text_fill_premium_t3(self) -> None:
        self.tf.add('mat', 1)
        self.tf.add('match', 1)
        self.tf.add('merch', 1)
        self.tf.add('ab', 1)
        self.tf.add('act', 1)
        self.tf.add('absolve', 1)
        self.tf.add('zen', 1)
        self.tf.add('zee', 1)

        self.assertEqual('match', self.tf.text_fill_premium('matc'))
        self.assertEqual('merch', self.tf.text_fill_premium('me'))

        self.assertIsNone(self.tf.text_fill_premium('zeee'))
        self.assertIsNone(self.tf.text_fill_premium('mab'))

        self.assertTrue((s := self.tf.text_fill_premium('ma')) == 'mat' or s == 'match')
        self.assertTrue((s := self.tf.text_fill_premium('ab')) == 'ab' or s == 'absolve')
        self.assertTrue((s := self.tf.text_fill_premium('z')) == 'zen' or s == 'zee')
    
    def test_text_fill_premium_t4(self) -> None:
        self.tf.add('m', 1)
        self.tf.add('a', 2)
        self.tf.add('z', 2)
        self.tf.add('b', 3)
        self.tf.add('c', 3)

        self.assertEqual('m', self.tf.text_fill_premium('m'))
        self.assertEqual('a', self.tf.text_fill_premium('a'))

        self.assertIsNone(self.tf.text_fill_premium('x'))
    
    def test_text_fill_premium_t5(self) -> None:
        self.tf.add('a', 1)
        self.tf.add('ab', 3)
        self.tf.add('absolve', 2)
        self.tf.add('absolved', 4)

        self.assertEqual('absolved', self.tf.text_fill_premium('a'))
        self.assertEqual('absolved', self.tf.text_fill_premium('ab'))
        self.assertEqual('absolved', self.tf.text_fill_premium('abs'))
    
    def test_text_fill_premium_t6(self) -> None:
        self.tf.add('a', 4)
        self.tf.add('ab', 1)
        self.tf.add('absolve', 3)
        self.tf.add('absolved', 2)

        self.assertEqual('a', self.tf.text_fill_premium('a'))
        self.assertEqual('absolve', self.tf.text_fill_premium('ab'))
        self.assertEqual('absolve', self.tf.text_fill_premium('abs'))
        self.assertEqual('absolved', self.tf.text_fill_premium('absolved'))
    
    def test_text_fill_premium_t7(self) -> None:
        self.tf.add('a', 4)
        self.tf.add('ab', 3)
        self.tf.add('absolve', 2)
        self.tf.add('absolved', 1)

        self.assertEqual('a', self.tf.text_fill_premium('a'))
        self.assertEqual('ab', self.tf.text_fill_premium('ab'))
        self.assertEqual('absolve', self.tf.text_fill_premium('abs'))
        self.assertEqual('absolved', self.tf.text_fill_premium('absolved'))
    
    def test_text_fill_premium_t8(self) -> None:
        self.tf.add('m', 1)
        self.tf.add('a', 2)
        self.tf.add('z', 2)
        self.tf.add('b', 3)
        self.tf.add('y', 3)

        self.assertEqual('m', self.tf.text_fill_premium('m'))
        self.assertEqual('a', self.tf.text_fill_premium('a'))
        self.assertEqual('b', self.tf.text_fill_premium('b'))
        self.assertEqual('z', self.tf.text_fill_premium('z'))
        self.assertEqual('y', self.tf.text_fill_premium('y'))

if __name__ == "__main__":
    unittest.main()