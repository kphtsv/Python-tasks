import unittest

import calculator

# название заканчивается на Test, нейминг
class TestCalculator(unittest.TestCase):
    def test1(self):
        art_width, art_height = calculator.calc_art_size(3, (2, 4))
        self.assertEqual(art_width, 3)
        self.assertEqual(art_height, 6)

    def test2(self):
        width, height = 2, 4
        art_width, art_height = calculator.calc_art_size(3, (width, height))
        self.assertAlmostEqual(width / height, art_width / art_height)

    def test3(self):
        width, height = 1272, 901
        art_width, art_height = calculator.calc_art_size(24, (width, height))
        self.assertAlmostEqual(width / height, art_width / art_height)