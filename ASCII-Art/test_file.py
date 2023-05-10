import ascii_converter.file_processor
from ascii_converter import *


def run():
    # art = ascii_converter.image_processor.to_art_from_file('images\\aa.png', 150)
    # img = ascii_converter.file_processor.write_art_to_image(art)
    # ascii_converter.file_processor.save_image(img, 'images\\grad_processed.png')

    # print(ascii_converter.file_processor.byte_format(14))
    # print(ascii_converter.file_processor.byte_format(189))

    rgb_matrix = ascii_converter.image_processor.to_ansi_art_from_file('images\\gradient.jpg', 150)
    img = ascii_converter.file_processor.write_color_art_to_image(rgb_matrix)
    ascii_converter.file_processor.save_image(img, 'images\\grad_processed.png')
    pass

run()
