import unittest
from PIL import Image
import image_processor


class ImageProcessorTest(unittest.TestCase):
    def test_flatten_slice(self):
        rgb_img = Image.open('../images/small_image_bw.png').convert('RGB')
        row = ((0, 0.5), (2, 0.5))
        column = ((1, 0), (1, 0.5))

        supposed_brightness = 0.25 + 0.5 * 0.5 + 0.25 * 0.6
        self.assertAlmostEqual(supposed_brightness, image_processor.flatten_slice(row, column, rgb_img), delta=1e-2)

    def test_process(self):
        filename_in = '../images/small_image_bw.png'
        str_len = 4

        supposed_art = 'vv``\n++vv\nvvff\nccvv\nvvbb\n$$vv\n'
        actual_art = image_processor.process(filename_in, str_len, False)
        self.assertEqual(supposed_art, actual_art)

