from wiki_walker import *
import unittest


class WikiWalkerGradingTests(unittest.TestCase):
    # =================================================
    # Test Configuration
    # =================================================

    # The size of the lattice to test with
    LATTICE_SIZE = 1000

    # Used as the basic empty WikiWalker to test.
    # The setUp() method is run before every test.
    def setUp(self) -> None:
        ''' '''
        self.ww = WikiWalker()

    # Sets up the structure of the site map for the
    # basic WikiWalker
    def setup_ww(self) -> None:
        self.ww.add_article('A', ['B', 'C'])
        self.ww.add_article('B', ['A', 'C'])
        self.ww.add_article('C', ['D', 'E'])
        self.ww.add_article('D', ['B', 'F'])
        self.ww.add_article('E', ['F'])

    def setup_ww_tree(self) -> None:
        self.ww.add_article('A', ['B', 'C', 'D'])
        self.ww.add_article('B', ['E', 'F'])
        self.ww.add_article('C', ['G', 'H'])
        self.ww.add_article('D', ['I'])
        self.ww.add_article('H', ['K'])

    def setup_ww_cycle(self) -> None:
        self.ww.add_article('A', ['B'])
        self.ww.add_article('B', ['C'])
        self.ww.add_article('C', ['D'])
        self.ww.add_article('D', ['A'])

    def setup_ww_islands(self) -> None:
        self.ww.add_article('A', ['B', 'C'])
        self.ww.add_article('B', ['C', 'D'])
        self.ww.add_article('D', ['E'])
        self.ww.add_article('F', ['G', 'H'])
        self.ww.add_article('G', ['K'])

    def setup_big_lattice(self) -> None:
        for i in range(WikiWalkerGradingTests.LATTICE_SIZE):
            self.ww.add_article(f'{i}', [f'{i + 1}', f'{i + 2}'])

    # =================================================
    # Unit Tests
    # =================================================

    def test_add_article(self) -> None:
        self.setup_ww()

    def test_has_path(self) -> None:
        self.setup_ww()

        self.assertTrue(self.ww.has_path('A', 'A'))
        self.assertTrue(self.ww.has_path('A', 'B'))
        self.assertTrue(self.ww.has_path('B', 'A'))
        self.assertTrue(self.ww.has_path('A', 'F'))
        self.assertTrue(self.ww.has_path('E', 'F'))
        self.assertTrue(self.ww.has_path('D', 'E'))
        self.assertFalse(self.ww.has_path('F', 'E'))
        self.assertFalse(self.ww.has_path('E', 'D'))

    def test_has_path_t1(self) -> None:
        self.setup_ww_tree()

        self.assertTrue(self.ww.has_path('A', 'A'))
        self.assertTrue(self.ww.has_path('A', 'B'))
        self.assertTrue(self.ww.has_path('B', 'F'))
        self.assertTrue(self.ww.has_path('A', 'K'))
        self.assertTrue(self.ww.has_path('C', 'K'))
        self.assertFalse(self.ww.has_path('E', 'D'))
        self.assertFalse(self.ww.has_path('B', 'A'))
        self.assertFalse(self.ww.has_path('E', 'F'))

    def test_has_path_t2(self) -> None:
        self.setup_ww_cycle()

        self.assertTrue(self.ww.has_path('A', 'A'))
        self.assertTrue(self.ww.has_path('A', 'B'))
        self.assertTrue(self.ww.has_path('B', 'B'))
        self.assertTrue(self.ww.has_path('B', 'A'))
        self.assertTrue(self.ww.has_path('C', 'A'))

    def test_has_path_t3(self) -> None:
        self.setup_ww_islands()

        self.assertTrue(self.ww.has_path('A', 'A'))
        self.assertTrue(self.ww.has_path('A', 'B'))
        self.assertTrue(self.ww.has_path('B', 'E'))
        self.assertFalse(self.ww.has_path('B', 'A'))
        self.assertFalse(self.ww.has_path('A', 'F'))
        self.assertFalse(self.ww.has_path('F', 'A'))
        self.assertFalse(self.ww.has_path('G', 'D'))
        self.assertFalse(self.ww.has_path('D', 'G'))

    def test_clickthroughs(self) -> None:
        self.setup_ww()

        self.assertEqual(0, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(0, self.ww.clickthroughs('B', 'A'))
        self.assertEqual(-1, self.ww.clickthroughs('A', 'A'))
        self.assertEqual(-1, self.ww.clickthroughs('A', 'D'))

    def test_clickthroughs_t1(self) -> None:
        self.setup_ww_tree()

        self.assertEqual(0, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(0, self.ww.clickthroughs('D', 'I'))
        self.assertEqual(-1, self.ww.clickthroughs('B', 'C'))
        self.assertEqual(-1, self.ww.clickthroughs('C', 'K'))
        self.assertEqual(-1, self.ww.clickthroughs('B', 'A'))
        self.assertEqual(-1, self.ww.clickthroughs('A', 'A'))

    def test_clickthroughs_t2(self) -> None:
        self.setup_ww_cycle()

        self.assertEqual(0, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(0, self.ww.clickthroughs('D', 'A'))
        self.assertEqual(-1, self.ww.clickthroughs('C', 'B'))
        self.assertEqual(-1, self.ww.clickthroughs('C', 'C'))

    def test_clickthroughs_t3(self) -> None:
        self.setup_ww_islands()

        self.assertEqual(0, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(0, self.ww.clickthroughs('B', 'C'))
        self.assertEqual(0, self.ww.clickthroughs('G', 'K'))
        self.assertEqual(-1, self.ww.clickthroughs('F', 'A'))
        self.assertEqual(-1, self.ww.clickthroughs('F', 'Z'))

    def test_trajectories(self) -> None:
        self.setup_ww()
        self.ww.log_trajectory(['A', 'B', 'C', 'D'])
        self.ww.log_trajectory(['A', 'C', 'D', 'F'])

        self.assertEqual(1, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(1, self.ww.clickthroughs('A', 'C'))
        self.assertEqual(1, self.ww.clickthroughs('B', 'C'))
        self.assertEqual(2, self.ww.clickthroughs('C', 'D'))

        self.ww.log_trajectory(['A', 'B', 'A', 'B', 'C'])

        self.assertEqual(3, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(1, self.ww.clickthroughs('B', 'A'))
        self.assertEqual(2, self.ww.clickthroughs('B', 'C'))

    def test_trajectories_t1(self) -> None:
        self.setup_ww_tree()
        self.ww.log_trajectory(['A', 'B', 'F'])
        self.ww.log_trajectory(['A', 'B', 'E'])
        self.ww.log_trajectory(['C', 'H', 'K'])
        self.ww.log_trajectory(['D', 'I'])

        self.assertEqual(2, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(1, self.ww.clickthroughs('D', 'I'))
        self.assertEqual(1, self.ww.clickthroughs('B', 'F'))
        self.assertEqual(1, self.ww.clickthroughs('B', 'E'))
        self.assertEqual(-1, self.ww.clickthroughs('B', 'A'))

    def test_trajectories_t2(self) -> None:
        self.setup_ww_cycle()
        self.ww.log_trajectory(['A', 'B'])
        self.ww.log_trajectory(['B', 'C', 'D'])
        self.ww.log_trajectory(['C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C'])

        self.assertEqual(3, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(3, self.ww.clickthroughs('B', 'C'))
        self.assertEqual(3, self.ww.clickthroughs('C', 'D'))
        self.assertEqual(3, self.ww.clickthroughs('C', 'D'))
        self.assertEqual(2, self.ww.clickthroughs('D', 'A'))
        self.assertEqual(-1, self.ww.clickthroughs('B', 'A'))

    def test_trajectories_t3(self) -> None:
        self.setup_ww_islands()
        self.ww.log_trajectory(['A', 'B', 'C'])
        self.ww.log_trajectory(['A', 'B', 'D', 'E'])
        self.ww.log_trajectory(['B', 'D', 'E'])
        self.ww.log_trajectory(['F', 'G'])
        self.ww.log_trajectory(['G', 'K'])

        self.assertEqual(2, self.ww.clickthroughs('A', 'B'))
        self.assertEqual(2, self.ww.clickthroughs('B', 'D'))
        self.assertEqual(1, self.ww.clickthroughs('F', 'G'))
        self.assertEqual(1, self.ww.clickthroughs('G', 'K'))
        self.assertEqual(-1, self.ww.clickthroughs('D', 'B'))
        self.assertEqual(-1, self.ww.clickthroughs('B', 'A'))

    def test_most_likely_trajectory(self) -> None:
        self.setup_ww()

        self.assertEqual(['B'], self.ww.most_likely_trajectory('A', 1))
        self.assertEqual(['B', 'A'], self.ww.most_likely_trajectory('A', 2))
        self.assertEqual(['B', 'A', 'B'], self.ww.most_likely_trajectory('A', 3))

        self.ww.log_trajectory(['A', 'B', 'C', 'D'])
        self.ww.log_trajectory(['A', 'C', 'D', 'F'])
        self.ww.log_trajectory(['A', 'B', 'A', 'B', 'C'])

        self.assertEqual(['B'], self.ww.most_likely_trajectory('A', 1))
        self.assertEqual(['B', 'C'], self.ww.most_likely_trajectory('A', 2))
        self.assertEqual(['B', 'C', 'D'], self.ww.most_likely_trajectory('A', 3))
        self.assertEqual(['B', 'C', 'D', 'F'], self.ww.most_likely_trajectory('A', 4))
        self.assertEqual(['B', 'C', 'D', 'F'], self.ww.most_likely_trajectory('A', 5))
        self.assertEqual(['B', 'C', 'D', 'F'], self.ww.most_likely_trajectory('A', 100))

    def test_most_likely_trajectory_t1(self) -> None:
        self.setup_ww_tree()
        self.ww.log_trajectory(['A', 'B', 'F'])
        self.ww.log_trajectory(['A', 'B', 'E'])
        self.ww.log_trajectory(['C', 'H', 'K'])
        self.ww.log_trajectory(['D', 'I'])

        self.assertEqual(['B'], self.ww.most_likely_trajectory('A', 1))
        self.assertEqual(['B', 'E'], self.ww.most_likely_trajectory('A', 2))
        self.assertEqual(['B', 'E'], self.ww.most_likely_trajectory('A', 3))
        self.assertEqual(['H'], self.ww.most_likely_trajectory('C', 1))
        self.assertEqual(['H', 'K'], self.ww.most_likely_trajectory('C', 2))
        self.assertEqual(['H', 'K'], self.ww.most_likely_trajectory('C', 3))

        self.ww.log_trajectory(['A', 'B', 'F'])

        self.assertEqual(['B', 'F'], self.ww.most_likely_trajectory('A', 3))

    def test_most_likely_trajectory_t2(self) -> None:
        self.setup_ww_cycle()
        self.ww.log_trajectory(['A', 'B'])
        self.ww.log_trajectory(['B', 'C', 'D'])
        self.ww.log_trajectory(['C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C'])

        self.assertEqual(['B'], self.ww.most_likely_trajectory('A', 1))
        self.assertEqual(['B', 'C'], self.ww.most_likely_trajectory('A', 2))
        self.assertEqual(['B', 'C', 'D'], self.ww.most_likely_trajectory('A', 3))
        self.assertEqual(['B', 'C', 'D', 'A'], self.ww.most_likely_trajectory('A', 4))
        self.assertEqual(['D', 'A', 'B', 'C'], self.ww.most_likely_trajectory('C', 4))

    def test_most_likely_trajectory_t3(self) -> None:
        self.setup_ww_islands()
        self.ww.log_trajectory(['A', 'C'])
        self.ww.log_trajectory(['A', 'C'])
        self.ww.log_trajectory(['A', 'B', 'D'])
        self.ww.log_trajectory(['F', 'G', 'K'])

        self.assertEqual(['C'], self.ww.most_likely_trajectory('A', 1))
        self.assertEqual(['C'], self.ww.most_likely_trajectory('A', 2))
        self.assertEqual(['C'], self.ww.most_likely_trajectory('A', 3))
        self.assertEqual(['D'], self.ww.most_likely_trajectory('B', 1))
        self.assertEqual(['D', 'E'], self.ww.most_likely_trajectory('B', 2))
        self.assertEqual(['D', 'E'], self.ww.most_likely_trajectory('B', 3))

    def test_lattice(self) -> None:
        self.setup_big_lattice()
        self.assertTrue(self.ww.has_path('0', '2'))
        self.assertTrue(self.ww.has_path('0', '3'))

    def test_lattice_t1(self) -> None:
        self.setup_big_lattice()
        self.assertTrue(self.ww.has_path('0', '960'))

    def test_lattice_t2(self) -> None:
        self.setup_big_lattice()

        for i in range(WikiWalkerGradingTests.LATTICE_SIZE):
            self.ww.log_trajectory([f'{i}', f'{i + 2}'])

        self.assertEqual(
            [f'{i}' for i in range(2, WikiWalkerGradingTests.LATTICE_SIZE, 2)],
            self.ww.most_likely_trajectory(
                '0', WikiWalkerGradingTests.LATTICE_SIZE // 2 - 1
            ),
        )


if __name__ == '__main__':
    unittest.main()