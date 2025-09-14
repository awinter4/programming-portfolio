from burnymon import Burnymon
from dampymon import Dampymon
from leafymon import Leafymon
from zappymon import Zappymon
from saalmon_arena import fight
from saalmon_subtypes import *
from linked_saalmonagerie import LinkedSaalmonagerie
import unittest
from typing import cast


class LinkedSaalmonagerieGradingTests(unittest.TestCase):
    # =================================================
    # Test Configuration
    # =================================================

    # Used as the basic empty LinkedSaalmonagerie to test
    # The setUp() method is run before every test
    def setUp(self) -> None:
        self.sm1 = LinkedSaalmonagerie()

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
    # 'zero-one-infinity' rule of testing) or tests for
    # proper error handling. Some of the below may be
    # organized for grading purposes instead.

    def test_diego(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.sm1.collect(Zappymon(1))
        print()
        print(self.sm1)

        self.sm1.rearrange(Dampymon(1).get_species(), 2)

        print(self.sm1)

    def test_len_t0(self) -> None:
        self.assertEqual(0, len(self.sm1))
        self.sm1.collect(Dampymon(1))
        self.assertEqual(1, len(self.sm1))

    def test_len_t1(self) -> None:
        self.assertEqual(0, len(self.sm1))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.assertEqual(2, len(self.sm1))

    def test_len_t2(self) -> None:
        self.assertEqual(0, len(self.sm1))
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(2))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.assertEqual(5, len(self.sm1))

    def test_len_t3(self) -> None:
        self.assertEqual(0, len(self.sm1))
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(2))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))
        self.assertEqual(9, len(self.sm1))

    def test_collect_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertTrue(self.sm1.contains_species('Burnymon'))
        self.assertFalse(self.sm1.contains_species('Zappymon'))
        self.assertEqual(2, len(self.sm1))
        self.assertEqual('Burnymon', self.sm1.get(1).get_species())

    def test_collect_t1(self) -> None:
        d1 = Dampymon(1)
        d2 = Dampymon(2)
        self.sm1.collect(d1)
        self.sm1.collect(d1)
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertEqual(1, self.sm1.get(0).get_level())
        self.sm1.collect(d2)
        self.assertEqual(2, self.sm1.get(0).get_level())
        self.assertEqual(1, len(self.sm1))

    def test_collect_t2(self) -> None:
        d1 = Dampymon(1)
        d2 = Dampymon(2)
        self.sm1.collect(d1)
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.sm1.collect(d2)
        self.assertEqual(2, self.sm1.get(0).get_level())
        self.sm1.collect(d1)
        self.assertEqual(2, self.sm1.get(0).get_level())
        self.assertEqual(1, len(self.sm1))
        print(self.sm1)

    def test_collect_t3(self) -> None:
        self.assertTrue(self.sm1.collect(Dampymon(1)))
        self.assertTrue(self.sm1.collect(Burnymon(2)))
        self.assertTrue(self.sm1.collect(Zappymon(3)))
        self.assertFalse(self.sm1.collect(Burnymon(4)))

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(2, self.sm1.get_species_index('Zappymon'))
        self.assertEqual(4, self.sm1.get(1).get_level())

    def test_collect_t4(self) -> None:
        leafy = Leafymon(3)
        self.assertEqual(0, len(self.sm1))
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(leafy)
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))
        self.sm1.collect(Dampymon(2))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(leafy)

        self.assertEqual(2, self.sm1.get(0).get_level())
        self.assertEqual(2, self.sm1.get(1).get_level())
        self.assertEqual(3, self.sm1.get(2).get_level())

    def test_release_species_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.assertEqual(2, len(self.sm1))

        self.sm1.release_species('Dampymon')

        self.assertEqual(1, len(self.sm1))
        self.assertTrue(self.sm1.contains_species('Burnymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))

    def test_release_species_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))

        self.assertTrue(self.sm1.release_species('Burnymon'))

        self.assertEqual(2, len(self.sm1))
        self.assertEqual('Dampymon', self.sm1.get(0).get_species())
        self.assertEqual('Leafymon', self.sm1.get(1).get_species())
        
        self.assertFalse(self.sm1.contains_species('Burnymon'))
        self.assertFalse(self.sm1.release_species('Burnymon'))

    def test_release_species_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))

        self.sm1.release_species('Dampymon')

        self.assertEqual(2, len(self.sm1))
        self.assertEqual('Burnymon', self.sm1.get(0).get_species())
        self.assertEqual('Leafymon', self.sm1.get(1).get_species())
        self.assertEqual(-1, self.sm1.get_species_index('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))
        self.assertRaises(IndexError, self.sm1.get, 2)

    def test_release_species_t3(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        self.sm1.release_species('Dampymon')
        self.sm1.release_species('Zappymon')

        self.assertEqual(7, len(self.sm1))
        self.assertEqual('Burnymon', self.sm1.get(0).get_species())
        self.assertEqual('Leafymon', self.sm1.get(1).get_species())
        self.assertEqual('Saalmon0', self.sm1.get(2).get_species())
        self.assertEqual('Saalmon1', self.sm1.get(3).get_species())

    def test_release_species_t4(self) -> None:
        self.assertFalse(self.sm1.release_species('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))

    def test_get_t0(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)

        self.sm1.collect(d1)
        self.sm1.collect(b1)

        self.assertEqual(d1, self.sm1.get(0))
        self.assertEqual(b1, self.sm1.get(1))

    def test_get_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.assertRaises(IndexError, self.sm1.get, -1)

    def test_get_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.assertRaises(IndexError, self.sm1.get, 2)

    def test_get_t3(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        self.assertEqual('Saalmon4', self.sm1.get(8).get_species())

    def test_get_mvp_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(3))
        self.sm1.collect(Leafymon(3))

        mvp = self.sm1.get_mvp()
        self.assertIsNotNone(mvp)
        mvp = cast(Saalmon, mvp)

        self.assertEqual('Leafymon', mvp.get_species())
        self.assertEqual(3, mvp.get_level())

    def test_get_mvp_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(3))
        self.sm1.collect(Leafymon(3))

        self.sm1.get(2).take_damage(10, DamageType.BASIC)
        mvp = self.sm1.get_mvp()
        self.assertIsNotNone(mvp)
        mvp = cast(Saalmon, mvp)

        self.assertEqual('Burnymon', mvp.get_species())
        self.assertEqual(3, mvp.get_level())

    def test_get_mvp_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(3))
        self.sm1.collect(Leafymon(3))

        self.sm1.get(2).take_damage(5, DamageType.BASIC)
        mvp = self.sm1.get_mvp()
        self.assertIsNotNone(mvp)
        mvp = cast(Saalmon, mvp)

        self.assertEqual('Burnymon', mvp.get_species())
        self.assertEqual(3, mvp.get_level())

    def test_get_mvp_t3(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(4))
        self.sm1.collect(Burnymon(3))

        self.sm1.get(2).take_damage(5, DamageType.BASIC)
        mvp = self.sm1.get_mvp()
        self.assertIsNotNone(mvp)
        mvp = cast(Saalmon, mvp)

        self.assertEqual('Zappymon', mvp.get_species())
        self.assertEqual(4, mvp.get_level())

    def test_remove_t0(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.assertEqual(2, len(self.sm1))

        self.sm1.remove(0)

        self.assertEqual(1, len(self.sm1))
        self.assertEqual(b1, self.sm1.get(0))

    def test_remove_t1(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)

        self.assertEqual(2, len(self.sm1))
        self.assertEqual(d1, self.sm1.remove(0))
        self.assertEqual(1, len(self.sm1))
        self.assertEqual(b1, self.sm1.remove(0))
        self.assertEqual(0, len(self.sm1))
        
        self.assertRaises(IndexError, self.sm1.remove, 0)

    def test_remove_t2(self) -> None:
        b1 = Burnymon(2)
        t1 = Saalmon0(1)
        t2 = Saalmon4(1)
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(b1)
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(t1)
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(t2)

        self.assertEqual(b1, self.sm1.remove(1))
        self.assertEqual(t1, self.sm1.remove(3))
        self.assertEqual(t2, self.sm1.remove(6))

    def test_get_species_index_contiains_species_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(-1, self.sm1.get_species_index('Leafymon'))
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Zappymon'))

    def test_get_species_index_contiains_species_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Dampymon(1))

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(-1, self.sm1.get_species_index('Leafymon'))
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Zappymon'))

    def test_get_species_index_contains_species_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(2, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(3, self.sm1.get_species_index('Zappymon'))
        self.assertEqual(4, self.sm1.get_species_index('Saalmon0'))
        self.assertEqual(8, self.sm1.get_species_index('Saalmon4'))
        self.assertEqual(-1, self.sm1.get_species_index('Saalmon5'))
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertTrue(self.sm1.contains_species('Saalmon2'))
        self.assertFalse(self.sm1.contains_species('Saalmon5'))

    def test_rearrange_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        self.sm1.rearrange('Leafymon', 0)

        self.assertEqual(1, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(2, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(0, self.sm1.get_species_index('Leafymon'))

    def test_rearrange_t1(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        e1 = Leafymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(e1)

        self.sm1.rearrange('Leafymon', 0)
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(e1)

        self.assertEqual(1, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(2, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(0, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(e1, self.sm1.get(0))
        self.assertEqual(d1, self.sm1.get(1))
        self.assertEqual(b1, self.sm1.get(2))

    def test_rearrange_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.sm1.collect(Zappymon(1))

        self.sm1.rearrange('Dampymon', 0)
        self.sm1.rearrange('Zappymon', 3)

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(2, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(3, self.sm1.get_species_index('Zappymon'))

    def test_rearrange_t3(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        e1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(e1)
        self.sm1.collect(z1)

        self.sm1.rearrange('Burnymon', 1)
        self.sm1.rearrange('Leafymon', 1)

        self.assertEqual(d1, self.sm1.get(0))
        self.assertEqual(e1, self.sm1.get(1))
        self.assertEqual(b1, self.sm1.get(2))
        self.assertEqual(z1, self.sm1.get(3))

    def test_rearrange_t4(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        e1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(e1)
        self.sm1.collect(z1)

        self.sm1.rearrange('Burnymon', 3)

        self.assertEqual(d1, self.sm1.get(0))
        self.assertEqual(e1, self.sm1.get(1))
        self.assertEqual(z1, self.sm1.get(2))
        self.assertEqual(b1, self.sm1.get(3))

    def test_rearrange_t5(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        self.sm1.rearrange('Dampymon', 8)
        self.sm1.rearrange('Saalmon4', 0)

        self.assertEqual(8, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(2, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(3, self.sm1.get_species_index('Zappymon'))
        self.assertEqual(4, self.sm1.get_species_index('Saalmon0'))
        self.assertEqual(0, self.sm1.get_species_index('Saalmon4'))
        self.assertEqual(-1, self.sm1.get_species_index('Saalmon5'))

    def test_rearrange_t6(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.assertRaises(IndexError, self.sm1.rearrange, 'Leafymon', 4)

    def test_rearrange_t7(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        e1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(e1)
        self.sm1.collect(z1)

        self.sm1.remove(2)
        self.sm1.rearrange('Dampymon', 2)

        self.assertEqual(b1, self.sm1.get(0))
        self.assertEqual(z1, self.sm1.get(1))
        self.assertEqual(d1, self.sm1.get(2))
        self.assertEqual(-1, self.sm1.get_species_index('Leafymon'))

    def test_clone_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        copy = self.sm1.clone()
        self.assertEqual(3, len(copy))
        
        self.sm1.get(0).take_damage(5, DamageType.BASIC)
        self.assertEqual(Dampymon.starting_health - 5, self.sm1.get(0).get_health())
        self.assertEqual(Dampymon.starting_health, copy.get(0).get_health())
        
        self.sm1.rearrange('Leafymon', 0)
        self.assertEqual(0, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(2, copy.get_species_index('Leafymon'))

    def test_clone_t1(self) -> None:
        copy = self.sm1.clone()
        self.assertEqual(0, len(copy))
        copy.collect(Dampymon(1))

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(0, copy.get_species_index('Dampymon'))
        self.assertEqual(-1, self.sm1.get_species_index('Dampymon'))
    
    def test_clone_t2(self) -> None:
        d1 = Dampymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        copy = self.sm1.clone()
        copy.collect(d1)
        self.sm1.collect(d1)

        self.assertEqual(9, len(copy))
        self.assertEqual(1, self.sm1.get(0).get_level())
        self.assertEqual(1, copy.get(0).get_level())

    def test_trade_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Leafymon(1))
        self.sm1.trade(sm2)
        
        self.assertEqual(2, len(sm2))
        self.assertEqual(1, len(self.sm1))
        self.assertTrue(self.sm1.contains_species('Leafymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))
        self.assertTrue(sm2.contains_species('Dampymon'))
        self.assertFalse(sm2.contains_species('Leafymon'))
                        
    def test_trade_t1(self) -> None:
        sm2 = LinkedSaalmonagerie()
        self.sm1.trade(sm2)
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertFalse(sm2.contains_species('Dampymon'))
        
        sm2.trade(self.sm1)
        self.assertTrue(sm2.contains_species('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))

    def test_trade_t2(self) -> None:
        sm2 = LinkedSaalmonagerie()
        sm3 = LinkedSaalmonagerie()
        
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        self.sm1.trade(sm2)
        sm2.trade(sm3)

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(0, len(sm2))
        self.assertEqual(9, len(sm3))

    def test_equals_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Dampymon(1))
        sm2.collect(Burnymon(1))
        
        self.assertEqual(self.sm1, sm2)
        sm2.rearrange('Burnymon', 0)
        self.assertNotEqual(self.sm1, sm2)

    def test_equals_t1(self) -> None:
        sm2 = LinkedSaalmonagerie()
        self.assertEqual(self.sm1, sm2)

    def test_equals_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = self.sm1.clone()

        self.assertEqual(self.sm1, sm2)
        self.assertEqual(self.sm1, self.sm1)

    def test_equals_t3(self) -> None:
        sm2 = LinkedSaalmonagerie()
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        sm2.collect(Dampymon(1))
        sm2.collect(Burnymon(1))
        sm2.collect(Leafymon(3))
        sm2.collect(Zappymon(2))
        sm2.collect(Saalmon0(1))
        sm2.collect(Saalmon1(1))
        sm2.collect(Saalmon2(1))
        sm2.collect(Saalmon3(1))
        sm2.collect(Saalmon4(1))

        self.assertNotEqual(self.sm1, sm2)
        sm2.collect(Burnymon(2))
        self.assertEqual(self.sm1, sm2)

    def test_equals_t4(self) -> None:
        sm2 = LinkedSaalmonagerie()
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(3))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))

        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(1))
        sm2.collect(Leafymon(3))
        sm2.collect(Zappymon(2))
        sm2.collect(Saalmon0(1))
        sm2.collect(Saalmon1(1))
        sm2.collect(Saalmon2(1))
        sm2.collect(Saalmon3(1))
        sm2.collect(Saalmon4(1))

        self.sm1.remove(0)
        sm2.remove(1)
        self.assertEqual(self.sm1, sm2)

    # =================================================
    # Integration Tests
    # =================================================

    def test_fight_t0(self) -> None:
        self.sm1.collect(Dampymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Dampymon(1))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(0, len(sm2))

    def test_fight_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Burnymon(1))
        sm2.collect(Dampymon(1))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(0, len(sm2))

    def test_fight_t2(self) -> None:
        self.sm1.collect(Dampymon(3))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(1))
        sm2.collect(Zappymon(1))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(1, len(sm2))

    def test_fight_t3(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Zappymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Burnymon(5))
        sm2.collect(Dampymon(5))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(1, len(sm2))

    def test_fight_t4(self) -> None:
        self.sm1.collect(Burnymon(5))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Dampymon(1))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(1, len(self.sm1))
        self.assertEqual(0, len(sm2))
        self.assertEqual(3, self.sm1.get(0).get_health())
        self.assertFalse(sm2.contains_species('Dampymon'))

    def test_fight_t5(self) -> None:
        self.sm1.collect(Dampymon(3))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.sm1.collect(Zappymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(3))
        sm2.collect(Zappymon(3))
        sm2.collect(Leafymon(3))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(0, len(self.sm1))
        self.assertEqual(2, len(sm2))

    def test_fight_t6(self) -> None:
        self.sm1.collect(Dampymon(3))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.sm1.collect(Zappymon(1))

        sm2 = LinkedSaalmonagerie()
        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(3))
        sm2.collect(Zappymon(3))
        sm2.collect(Leafymon(3))
        
        fight(self.sm1, sm2, False)

        self.assertEqual(8, sm2.get(0).get_health())
        self.assertEqual('Zappymon', sm2.get(0).get_species())
        self.assertEqual(2, sm2.get(1).get_health())
        self.assertEqual('Leafymon', sm2.get(1).get_species())

    def test_iterator_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        iterator = iter(self.sm1)
        self.assertIs(iterator.node, self.sm1.sentinel.next_node)

        self.assertEqual('Dampymon', iterator.__next__().get_species())
        self.assertEqual('Burnymon', iterator.__next__().get_species())
        self.assertEqual('Leafymon', iterator.__next__().get_species())
        self.assertRaises(StopIteration, iterator.__next__)

    def test_iterator_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        iterator = iter(self.sm1)
        self.sm1.collect(Dampymon(2))

        self.assertIs(iterator.node, self.sm1.sentinel.next_node)
        d1 = iterator.__next__()
        self.assertEqual('Dampymon', d1.get_species())
        self.assertEqual(2, d1.get_level())

    def test_iterator_t2(self) -> None:
        saalmon = [
            Dampymon(1),
            Burnymon(1),
            Leafymon(1),
            Zappymon(1),
            Saalmon0(1),
            Saalmon1(1),
            Saalmon2(1),
            Saalmon3(1),
            Saalmon4(1)
        ]

        for s in saalmon:
            self.sm1.collect(s)

        iterator = iter(self.sm1)

        for s in saalmon:
            self.assertIs(s, iterator.__next__())

        self.assertRaises(StopIteration, iterator.__next__)

    def test_iterator_t3(self) -> None:
        saalmon = [
            Dampymon(1),
            Burnymon(1),
            Leafymon(1),
            Zappymon(1),
            Saalmon0(1),
            Saalmon1(1),
            Saalmon2(1),
            Saalmon3(1),
            Saalmon4(1)
        ]

        for s in saalmon:
            self.sm1.collect(s)

        i = 0
        for s in self.sm1:
            self.assertIs(s, saalmon[i])
            i += 1

        self.assertEqual(i, len(saalmon))

    def test_iterator_t4(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        iterator = iter(self.sm1)
        self.sm1.remove(1)

        self.assertEqual('Dampymon', iterator.__next__().get_species())
        self.assertEqual('Leafymon', iterator.__next__().get_species())
        self.assertRaises(StopIteration, iterator.__next__)

    def test_iterator_t5(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        iterator = iter(self.sm1)
        self.sm1.rearrange('Leafymon', 1)

        self.assertEqual('Dampymon', iterator.__next__().get_species())
        self.assertEqual('Leafymon', iterator.__next__().get_species())
        self.assertEqual('Burnymon', iterator.__next__().get_species())
        self.assertRaises(StopIteration, iterator.__next__)

    def test_iterator_t6(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        l1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)
        self.sm1.collect(z1)
        self.sm1.rearrange('Zappymon', 0)
        self.sm1.rearrange('Burnymon', 3)

        saalmon = [z1, d1, l1, b1]
        iterator = iter(self.sm1)

        for s in saalmon:
            self.assertIs(s, iterator.__next__())

        self.assertRaises(StopIteration, iterator.__next__)

    def test_iterator_t7(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        l1 = Leafymon(1)
        
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)
        sm2 = LinkedSaalmonagerie()

        it1 = iter(self.sm1)
        self.assertIs(d1, it1.__next__())
        it2 = iter(sm2)

        self.sm1.trade(sm2)

        self.assertIs(b1, it1.__next__())
        self.assertIs(l1, it1.__next__())
        self.assertRaises(StopIteration, it1.__next__)
        self.assertRaises(StopIteration, it2.__next__)
        self.assertEqual(0, len(self.sm1))
        self.assertEqual(3, len(sm2))

    def test_iterator_t8(self) -> None:
        saalmon1 = [
            Dampymon(1),
            Leafymon(1),
            Burnymon(1)
        ]
        saalmon2 = [
            Zappymon(1),
            Burnymon(1),
            Leafymon(1)
        ]
        sm2 = LinkedSaalmonagerie()

        for s1, s2 in zip(saalmon1, saalmon2):
            self.sm1.collect(s1)
            sm2.collect(s2)
        
        it1 = iter(self.sm1)
        it2 = iter(sm2)
        self.sm1.trade(sm2)

        for s1, s2 in zip(saalmon1, saalmon2):
            self.assertIs(s1, it1.__next__())
            self.assertIs(s2, it2.__next__())

        self.assertRaises(StopIteration, it1.__next__)
        self.assertRaises(StopIteration, it2.__next__)

    def test_iterator_t9(self) -> None:
        saalmon1 = [
            Dampymon(1),
            Leafymon(1),
            Burnymon(1)
        ]
        saalmon2 = [
            Zappymon(1),
            Burnymon(1),
            Leafymon(1)
        ]
        sm2 = LinkedSaalmonagerie()

        for s1, s2 in zip(saalmon1, saalmon2):
            self.sm1.collect(s1)
            sm2.collect(s2)
        
        self.sm1.trade(sm2)
        it1 = iter(self.sm1)
        it2 = iter(sm2)

        for s1, s2 in zip(saalmon1, saalmon2):
            self.assertIs(s1, it2.__next__())
            self.assertIs(s2, it1.__next__())

        self.assertRaises(StopIteration, it1.__next__)
        self.assertRaises(StopIteration, it2.__next__)

    def test_iterator_t10(self) -> None:
        saalmon = [
            Dampymon(1),
            Burnymon(1),
            Leafymon(1)
        ]

        for s in saalmon:
            self.sm1.collect(s)
        sm2 = self.sm1.clone()

        it1 = iter(self.sm1)
        it2 = iter(sm2)

        for s in saalmon:
            self.assertIs(s, it1.__next__())
            s2 = it2.__next__()
            self.assertIsNot(s, s2)
            self.assertEqual(s, s2)

        self.assertRaises(StopIteration, it1.__next__)
        self.assertRaises(StopIteration, it2.__next__)

    def test_iterator_t11(self) -> None:
        saalmon = [
            Dampymon(1),
            Zappymon(1),
            Leafymon(1),
            Burnymon(1)
        ]

        for s in saalmon:
            self.sm1.collect(s)

        i = 0
        for s1 in self.sm1:
            for s, s2 in zip(saalmon, self.sm1):
                self.assertIs(saalmon[i], s1)
                self.assertIs(s, s2)

            i += 1
    

if __name__ == '__main__':
    unittest.main()