import unittest
from PIL import Image
from ascii_converter import image_processor


class ImageProcessorTest(unittest.TestCase):
    def test_flatten_brightness(self):
        rgb_img = Image.open('../images/small_image_bw.png').convert('RGB')
        row = ((0, 0.5), (2, 0.5))
        column = ((1, 0), (1, 0.5))

        supposed_brightness = 0.25 + 0.5 * 0.5 + 0.25 * 0.6
        self.assertAlmostEqual(supposed_brightness, image_processor.flatten_slice_brightness(row, column, rgb_img),
                               delta=1e-2)

    def test_flatten_color(self):
        rgb_img = Image.open('../images/test.png').convert('RGB')
        row = ((2, 0), (3, 0))
        column = ((0, 0), (1, 0.5))

        r_s, g_s, b_s = 255, 53, 5
        r_a, g_a, b_a = image_processor.flatten_slice_color(row, column, rgb_img)

        self.assertEqual(r_s, r_a)
        self.assertEqual(g_s, g_a)
        self.assertEqual(b_s, b_a)

    def test_to_ascii_art(self):
        filename_in = '../images/small_image_bw.png'
        str_len = 4

        supposed_art = 'vv``\n++vv\nvvff\nccvv\nvvbb\n$$vv\n'
        actual_art = image_processor.to_ascii_art_from_file(filename_in, str_len, False)
        self.assertEqual(supposed_art, actual_art)

    def test_to_ansi_art(self):
        filename_in = '../images/small_image.png'
        str_len = 2

        supposed_rgb_matrix = [
            [(255, 135, 135), (255, 215, 175)],
            [(215, 215, 95), (135, 215, 135)],
            [(0, 95, 175), (135, 95, 175)]
        ]
        actual_rgb_matrix = image_processor.to_ansi_art_from_file(filename_in, str_len)
        self.assertEqual(supposed_rgb_matrix, actual_rgb_matrix)
