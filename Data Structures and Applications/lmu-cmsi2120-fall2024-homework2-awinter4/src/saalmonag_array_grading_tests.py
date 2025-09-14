from saalmon_subtypes import *
from damage_type import DamageType
from dampymon import Dampymon
from burnymon import Burnymon
from leafymon import Leafymon
from zappymon import Zappymon
from saalmonag_array import *
from saalmon_arena import fight
import unittest
from typing import cast

class SaalmonagArrayGradingTests(unittest.TestCase):
    # =================================================
    # Test Configuration
    # =================================================

    # Used as the basic empty SaalmonagArray to test the
    # setUp() method is run before every test
    def setUp(self) -> None:
        self.sm1 = SaalmonagArray()

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

    def test_size_t0(self) -> None:
        self.assertEqual(0, self.sm1.size())
        self.sm1.collect(Dampymon(1))
        self.assertEqual(1, self.sm1.size())

    def test_size_t1(self) -> None:
        self.assertEqual(0, self.sm1.size())
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.assertEqual(2, self.sm1.size())

    def test_size_t2(self) -> None:
        self.assertEqual(0, self.sm1.size())
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(2))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.assertEqual(5, self.sm1.size())

    def test_size_t3(self) -> None:
        self.assertEqual(0, self.sm1.size())
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(2))
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))
        self.assertEqual(9, self.sm1.size())

    def test_collect_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertTrue(self.sm1.contains_species('Burnymon'))
        self.assertFalse(self.sm1.contains_species('Zappymon'))
        self.assertEqual(2, self.sm1.size())
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
        self.assertEqual(1, self.sm1.size())

    def test_collect_t2(self) -> None:
        d1 = Dampymon(1)
        d2 = Dampymon(2)
        self.sm1.collect(d1)
        self.assertTrue(self.sm1.contains_species('Dampymon'))

        self.sm1.collect(d2)
        self.assertEqual(2, self.sm1.get(0).get_level())

        self.sm1.collect(d1)
        self.assertEqual(2, self.sm1.get(0).get_level())
        self.assertEqual(1, self.sm1.size())

    def test_collect_t3(self) -> None:
        c1 = self.sm1.collect(Dampymon(1))
        c2 = self.sm1.collect(Burnymon(2))
        c3 = self.sm1.collect(Zappymon(3))
        c4 = self.sm1.collect(Burnymon(4))

        self.assertTrue(c1)
        self.assertTrue(c2)
        self.assertTrue(c3)
        self.assertFalse(c4)

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(2, self.sm1.get_species_index('Zappymon'))

        self.assertEqual(4, self.sm1.get(1).get_level())

    def test_collect_t4(self) -> None:
        l1 = Leafymon(3)
        self.assertEqual(0, self.sm1.size())
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(l1)
        self.sm1.collect(Zappymon(2))
        self.sm1.collect(Saalmon0(1))
        self.sm1.collect(Saalmon1(1))
        self.sm1.collect(Saalmon2(1))
        self.sm1.collect(Saalmon3(1))
        self.sm1.collect(Saalmon4(1))
        self.sm1.collect(Dampymon(2))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(l1)

        self.assertEqual(2, self.sm1.get(0).get_level())
        self.assertEqual(2, self.sm1.get(1).get_level())
        self.assertEqual(3, self.sm1.get(2).get_level())

    def test_release_species_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.assertEqual(2, self.sm1.size())

        self.sm1.release_species('Dampymon')
        self.assertEqual(1, self.sm1.size())
        self.assertTrue(self.sm1.contains_species('Burnymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))

    def test_release_species_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))

        rt1 = self.sm1.release_species('Burnymon')
        self.assertTrue(rt1)
        self.assertEqual(2, self.sm1.size())
        self.assertEqual('Dampymon', self.sm1.get(0).get_species())
        self.assertEqual('Leafymon', self.sm1.get(1).get_species())
        self.assertFalse(self.sm1.contains_species('Burnymon'))

        rt2 = self.sm1.release_species('Burnymon')
        self.assertFalse(rt2)

    def test_release_species_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(2))
        self.sm1.collect(Leafymon(3))

        self.sm1.release_species('Dampymon')
        self.assertEqual(2, self.sm1.size())
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
        self.assertEqual(7, self.sm1.size())
        self.assertEqual('Burnymon', self.sm1.get(0).get_species())
        self.assertEqual('Leafymon', self.sm1.get(1).get_species())
        self.assertEqual('Saalmon0', self.sm1.get(2).get_species())
        self.assertEqual('Saalmon1', self.sm1.get(3).get_species())

    def test_release_species_t4(self) -> None:
        self.sm1.release_species('Dampymon')
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

        result = self.sm1.get_mvp()
        self.assertIsNotNone(result)
        result = cast(Saalmon, result)

        self.assertEqual('Leafymon', result.get_species())
        self.assertEqual(3, result.get_level())

    def test_get_mvp_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(3))
        self.sm1.collect(Leafymon(3))
        self.sm1.get(2).take_damage(10, DamageType.BASIC)

        result = self.sm1.get_mvp()
        self.assertIsNotNone(result)
        result = cast(Saalmon, result)

        self.assertEqual('Burnymon', result.get_species())
        self.assertEqual(3, result.get_level())

    def test_get_mvp_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(3))
        self.sm1.collect(Leafymon(3))
        self.sm1.get(2).take_damage(5, DamageType.BASIC)

        result = self.sm1.get_mvp()
        self.assertIsNotNone(result)
        result = cast(Saalmon, result)

        self.assertEqual('Burnymon', result.get_species())
        self.assertEqual(3, result.get_level())

    def test_get_mvp_t3(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Leafymon(3))
        self.sm1.collect(Zappymon(4))
        self.sm1.collect(Burnymon(3))
        self.sm1.get(2).take_damage(5, DamageType.BASIC)

        result = self.sm1.get_mvp()
        self.assertIsNotNone(result)
        result = cast(Saalmon, result)

        self.assertEqual('Zappymon', result.get_species())
        self.assertEqual(4, result.get_level())

    def test_remove_t0(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.assertEqual(2, self.sm1.size())

        self.sm1.remove(0)
        self.assertEqual(1, self.sm1.size())
        self.assertEqual(b1, self.sm1.get(0))

    def test_remove_t1(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.assertEqual(2, self.sm1.size())

        self.assertEqual(d1, self.sm1.remove(0))
        self.assertEqual(1, self.sm1.size())

        self.assertEqual(b1, self.sm1.remove(0))
        self.assertEqual(0, self.sm1.size())
        
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

    def test_get_species_index_contains_species_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        self.assertEqual(0, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(1, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(-1, self.sm1.get_species_index('Leafymon'))

        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Zappymon'))

    def test_get_species_index_contains_species_t1(self) -> None:
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
        l1 = Leafymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)

        self.sm1.rearrange('Leafymon', 0)

        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)

        self.assertEqual(1, self.sm1.get_species_index('Dampymon'))
        self.assertEqual(2, self.sm1.get_species_index('Burnymon'))
        self.assertEqual(0, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(l1, self.sm1.get(0))
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
        l1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)
        self.sm1.collect(z1)

        self.sm1.rearrange('Burnymon', 1)
        self.sm1.rearrange('Leafymon', 1)

        self.assertEqual(d1, self.sm1.get(0))
        self.assertEqual(l1, self.sm1.get(1))
        self.assertEqual(b1, self.sm1.get(2))
        self.assertEqual(z1, self.sm1.get(3))

    def test_rearrange_t4(self) -> None:
        d1 = Dampymon(1)
        b1 = Burnymon(1)
        l1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)
        self.sm1.collect(z1)

        self.sm1.rearrange('Burnymon', 3)

        self.assertEqual(d1, self.sm1.get(0))
        self.assertEqual(l1, self.sm1.get(1))
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
        l1 = Leafymon(1)
        z1 = Zappymon(1)
        self.sm1.collect(d1)
        self.sm1.collect(b1)
        self.sm1.collect(l1)
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

        sm2 = self.sm1.clone()
        self.assertEqual(3, sm2.size())
        
        self.sm1.get(0).take_damage(5, DamageType.BASIC)
        self.assertEqual(Dampymon.starting_health - 5, self.sm1.get(0).get_health())
        self.assertEqual(Dampymon.starting_health, sm2.get(0).get_health())
        
        self.sm1.rearrange('Leafymon', 0)
        self.assertEqual(0, self.sm1.get_species_index('Leafymon'))
        self.assertEqual(2, sm2.get_species_index('Leafymon'))

    def test_clone_t1(self) -> None:
        sm2 = self.sm1.clone()
        self.assertEqual(0, sm2.size())

        sm2.collect(Dampymon(1))

        self.assertEqual(0, self.sm1.size())
        self.assertEqual(0, sm2.get_species_index('Dampymon'))
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

        sm2 = self.sm1.clone()
        sm2.collect(d1)
        self.sm1.collect(d1)

        self.assertEqual(9, sm2.size())
        self.assertEqual(1, self.sm1.get(0).get_level())
        self.assertEqual(1, sm2.get(0).get_level())

    def test_trade_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        
        sm2 = SaalmonagArray()
        sm2.collect(Leafymon(1))
        self.sm1.trade(sm2)
        
        self.assertEqual(2, sm2.size())
        self.assertEqual(1, self.sm1.size())
        self.assertTrue(self.sm1.contains_species('Leafymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))
        self.assertTrue(sm2.contains_species('Dampymon'))
        self.assertFalse(sm2.contains_species('Leafymon'))

    def test_trade_t1(self) -> None:
        sm2 = SaalmonagArray()
        self.sm1.trade(sm2)
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        self.assertTrue(self.sm1.contains_species('Dampymon'))
        self.assertFalse(sm2.contains_species('Dampymon'))

        sm2.trade(self.sm1)
        self.assertTrue(sm2.contains_species('Dampymon'))
        self.assertFalse(self.sm1.contains_species('Dampymon'))

    def test_trade_t2(self) -> None:
        sm2 = SaalmonagArray()
        sm3 = SaalmonagArray()

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

        self.assertEqual(0, self.sm1.size())
        self.assertEqual(0, sm2.size())
        self.assertEqual(9, sm3.size())

    def test_equals_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = SaalmonagArray()
        sm2.collect(Dampymon(1))
        sm2.collect(Burnymon(1))
        
        self.assertEqual(self.sm1, sm2)
        sm2.rearrange('Burnymon', 0)
        self.assertNotEqual(self.sm1, sm2)

    def test_equals_t1(self) -> None:
        sm2 = SaalmonagArray()
        self.assertEqual(self.sm1, sm2)

    def test_equals_t2(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = self.sm1.clone()
        self.assertEqual(self.sm1, sm2)

    def test_equals_t3(self) -> None:
        sm2 = SaalmonagArray()

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
        sm2 = SaalmonagArray()

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

        self.assertNotEqual(self.sm1, sm2)
        self.sm1.remove(0)
        sm2.remove(1)
        self.assertEqual(self.sm1, sm2)

    # =================================================
    # Integration Tests
    # =================================================

    def test_fight_t0(self) -> None:
        self.sm1.collect(Dampymon(1))
        sm2 = SaalmonagArray()
        sm2.collect(Dampymon(1))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(0, self.sm1.size())
        self.assertEqual(0, sm2.size())

    def test_fight_t1(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))

        sm2 = SaalmonagArray()
        sm2.collect(Burnymon(1))
        sm2.collect(Dampymon(1))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(0, self.sm1.size())
        self.assertEqual(0, sm2.size())

    def test_fight_t2(self) -> None:
        self.sm1.collect(Dampymon(3))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))

        sm2 = SaalmonagArray()
        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(1))
        sm2.collect(Zappymon(1))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(0, self.sm1.size())
        self.assertEqual(1, sm2.size())

    def test_fight_t3(self) -> None:
        self.sm1.collect(Dampymon(1))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Zappymon(1))
        
        sm2 = SaalmonagArray()
        sm2.collect(Burnymon(5))
        sm2.collect(Dampymon(5))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(0, self.sm1.size())
        self.assertEqual(1, sm2.size())

    def test_fight_t4(self) -> None:
        self.sm1.collect(Burnymon(5))
        
        sm2 = SaalmonagArray()
        sm2.collect(Dampymon(1))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(1, self.sm1.size())
        self.assertEqual(0, sm2.size())
        self.assertEqual(3, self.sm1.get(0).get_health())
        self.assertFalse(sm2.contains_species('Dampymon'))

    def test_fight_t5(self) -> None:
        self.sm1.collect(Dampymon(3))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.sm1.collect(Zappymon(1))

        sm2 = SaalmonagArray()
        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(3))
        sm2.collect(Zappymon(3))
        sm2.collect(Leafymon(3))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(0, self.sm1.size())
        self.assertEqual(2, sm2.size())

    def test_fight_t6(self) -> None:
        self.sm1.collect(Dampymon(3))
        self.sm1.collect(Burnymon(1))
        self.sm1.collect(Leafymon(1))
        self.sm1.collect(Zappymon(1))

        sm2 = SaalmonagArray()
        sm2.collect(Burnymon(3))
        sm2.collect(Dampymon(3))
        sm2.collect(Zappymon(3))
        sm2.collect(Leafymon(3))
        
        fight(self.sm1, sm2, False)
        self.assertEqual(8, sm2.get(0).get_health())
        self.assertEqual('Zappymon', sm2.get(0).get_species())
        self.assertEqual(2, sm2.get(1).get_health())
        self.assertEqual('Leafymon', sm2.get(1).get_species())

if __name__ == '__main__':
    unittest.main()