import re

import ascii_converter.file_processor
from ascii_converter import *


def run():
    # art = ascii_converter.image_processor.to_art_from_file('images\\aa.png', 150)
    # img = ascii_converter.file_processor.write_art_to_image(art)
    # ascii_converter.file_processor.save_image(img, 'images\\grad_processed.png')

    # print(ascii_converter.file_processor.byte_format(14))
    # print(ascii_converter.file_processor.byte_format(189))

    # rgb_matrix = ascii_converter.image_processor.to_ansi_art_from_file('images\\gradient.jpg', 150)
    # img = ascii_converter.file_processor.write_color_art_to_image(rgb_matrix)
    # ascii_converter.file_processor.save_image(img, 'images\\grad_processed.png')
    #

    # input_dir = 'videos\\short_video.mp4'
    # output_dir = 'videos\\short_video_processed.mp4'
    # saved = ascii_converter.file_processor.video_to_ascii(input_dir, 150)

    r, g, b = 56, 47, 25
    ansi_code = ascii_converter .ansi_color_converter.rgb_to_xterm_color(r, g, b)
    print(ansi_code)


def parse_xterm():
    with open('xterm.txt', 'r') as file:
        lines = file.read().split('\n')

    pattern = re.compile(r'([0-9]+).+rgb\(([0-9]+),([0-9]+),([0-9]+)\)')
    for line in lines:
        match = pattern.search(line)
        if match:
            number = match.group(1)
            r = match.group(2)
            g = match.group(3)
            b = match.group(4)
            print(f'{number}: ({r}, {g}, {b}),')


# run()
parse_xterm()
