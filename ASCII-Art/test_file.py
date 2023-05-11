import re

import ascii_converter.file_processor
from ascii_converter import *


def run():
    a = ascii_converter.calculator.rgb_to_ansi_color_code(208, 245, 255)
    print(a)


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


run()
# parse_xterm()
