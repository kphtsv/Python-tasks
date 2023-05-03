import unittest
from ascii_converter import calculator
from PIL import Image


class CalculatorTest(unittest.TestCase):
    def test_cuts(self):
        def test(str_length, width, supposed_cuts):
            actual_cuts = calculator.calc_cuts(str_length, width)
            for i in range(len(supposed_cuts)):
                pixel, fraction = actual_cuts[i]
                self.assertEqual(pixel + fraction, supposed_cuts[i])

        test(6, 3, [0, 0.5, 1, 1.5, 2, 2.5, 3])  # кусочки поменьше
        test(3, 6, [0, 2, 4, 6])  # кусочки побольше

    def test_art_sizes(self):
        def test(str_length, img_size):
            width, height = img_size
            art_width, art_height = calculator.calc_art_size(str_length, img_size)
            self.assertAlmostEqual(width / height,
                                   calculator.stretching_coefficient * art_width / art_height, delta=1e-1)

        test(24, (1272, 901))
        test(3, (2, 4))

        # self.test_art_size(5, (0, 1))  # такого не может быть
        # self.test_art_size(5, (1, 0))  # такого не может быть

    def test_all_rgb_to_brightness(self):
        def test(pixel, supposed_brightness):
            actual_brightness = calculator.rgb_to_brightness(*pixel)
            self.assertAlmostEqual(supposed_brightness, actual_brightness, delta=1e-2)

        rgb_img = Image.open('../images/small_image_bw.png').convert('RGB')
        test(rgb_img.getpixel((0, 0)), 0.5)
        test(rgb_img.getpixel((0, 5)), 0)

    # нет теста на brightness_to_ascii

    def test_pixel_is_inside(self):
        row = ((0, 0.5), (2, 0.5))
        column = ((0, 1), (1, 1))

        self.assertTrue(calculator.pixel_is_inside((1, 0), row, column))
        self.assertTrue(calculator.pixel_is_inside((1, 1), row, column))
        self.assertTrue(calculator.pixel_is_inside((1, 2), row, column))

        self.assertFalse(calculator.pixel_is_inside((1, 3), row, column))
        self.assertFalse(calculator.pixel_is_inside((0, 0), row, column))
        self.assertFalse(calculator.pixel_is_inside((0, 1), row, column))
        self.assertFalse(calculator.pixel_is_inside((2, 1), row, column))

    def test_calc_pixel_surface(self):
        row = ((0, 0.5), (2, 0.5))
        column = ((0, 1), (1, 0.5))

        self.assertAlmostEqual(0.25, calculator.calc_pixel_surface(row, column, (1, 0)))
        self.assertAlmostEqual(0.5, calculator.calc_pixel_surface(row, column, (1, 1)))
        self.assertAlmostEqual(0, calculator.calc_pixel_surface(row, column, (0, 0)))

    def test_calc_pixel_brightness(self):
        row = ((0, 0.5), (2, 0.5))
        column = ((0, 1), (1, 0.5))
        rgb_img = Image.open('../images/small_image_bw.png').convert('RGB')

        self.assertAlmostEqual(0.25, calculator.calc_pixel_brightness(row, column, rgb_img, (1, 0)), delta=1e-1)
        self.assertAlmostEqual(0.25, calculator.calc_pixel_brightness(row, column, rgb_img, (1, 1)), delta=1e-1)
