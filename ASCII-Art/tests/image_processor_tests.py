# import unittest
# from PIL import Image
# import image_processor
#
#
# class TestImageProcessor(unittest.TestCase):
#     # def test_on_edges(self):
#     #     self.a
#
#     def test_pixel_brightness(self):
#         row = ((1, 0), (1, 0.5))
#         column = ((1, 0), (1, 0.5))
#         img = Image.open('TestImages/small_image.png')
#         rgb_img = img.convert('RGB')
#         pixel_coord = (1, 1)
#
#         self.assertAlmostEqual(image_processor.calc_pixel_brightness(row, column, rgb_img, pixel_coord), 0.25)
#
#     def rgb_brightness_test():
#         img = Image.open('tests/TestImages/small_image.png')
#         rgb_img = img.convert('RGB')
#         pixel_coord = (1, 4)
#         r, g, b = rgb_img.getpixel(pixel_coord)
#
#         print(rgb_to_brightness(r, g, b))
#
#     def flatten_slice_test():
#         img = Image.open('tests/TestImages/test.png')
#         rgb_img = img.convert('RGB')
#
#         row = ((2, 0), (3, 0))
#         column = ((0, 0), (6, 1))
#
#         print(flatten_slice(row, column, rgb_img))
#
#     def test1():
#         row = ((0, 0), (1, 1.5))
#         column = ((1, 0), (1, 0.5))
#         img = Image.open('tests/TestImages/small_image.png')
#         rgb_img = img.convert('RGB')
#         pixel_coord = (0, 0)
#
#         print(calc_pixel_brightness(row, column, rgb_img, pixel_coord))
#
#     def test2():
#         row = ((0, 0), (1, 0))
#         column = ((1, 0.5), (2, 0))
#         img = Image.open('tests/TestImages/small_image.png')
#         rgb_img = img.convert('RGB')
#         pixel_coord = (1, 0)
#
#         print(pixel_is_inside(pixel_coord, row, column))
