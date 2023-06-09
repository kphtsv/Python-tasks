import math
from ascii_converter.ansi_color import ANSI_CODE_TO_COLOR

# TODO: pylint , coverage > 80%


def calc_cuts(str_length, width):
    """
    Вычисляет сечения по длине пикселей.
    :param str_length: int, кол-во сечений
    :param width: int, длина/ширина изображения
    :return: list, список сечений в формате (pix_num, frac):
        pix_num: номер пикселя, через который проходит сечение
        frac: процент от длины пикселя, где именно проходит сечение
    """
    cuts = []
    for c in range(0, str_length + 1):
        perfect_cut = (c / str_length) * width
        pixel_number = math.floor(perfect_cut)
        frac_part = perfect_cut - math.trunc(perfect_cut)
        cuts.append((pixel_number, frac_part))
    return cuts


stretching_coefficient = 0.5


def calc_art_size(str_length, img_size):
    """
    Вычисляет длину/высоту ASCII-арта в соответствии с пропорциями изображения.
    :param str_length: int - длина ASCII-арта
    :param img_size: (int, int) - размеры исходного изображения
    :return: (int, int) - длина, высота ASCII-арта
    """
    width, height = img_size
    art_width = str_length
    art_height = math.floor(stretching_coefficient * str_length * (height / width))
    return art_width, art_height


template = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def rgb_to_brightness(r, g, b, grayscale=True):
    """
    Вычисляет яркость полного пикселя на шкале [0;1]
    :param r: int - яркость красного
    :param g: int - яркость зеленого
    :param b: int - яркость синего
    :param grayscale: float - монохромен ли контекст запроса
    :return: float - яркость пикселя
    """
    if grayscale:
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    else:
        return (0.267 * r + 0.642 * g + 0.091 * b) / 255


def rgb_to_ansi_color(r, g, b):
    """
    Конвертирует r, g, b значения в ANSI-цвет.uh 766
    :param r: int - яркость красного
    :param g: int - яркость зеленого
    :param b: int - яркость синего
    :return: (int, int, int) - ANSI-цвет
    """
    return ANSI_CODE_TO_COLOR[rgb_to_ansi_color_code(r, g, b)]


def rgb_to_ansi_color_code(r, g, b):
    """
        Конвертирует r, g, b значения в код ANSI-цвета.
        :param r: int - яркость красного
        :param g: int - яркость зеленого
        :param b: int - яркость синего
        :return: int - номер ANSI-цвета
        """
    if r == g & g == b:
        if r < 8:
            return 16
        if r > 248:
            return 230
        return int(round(((r - 8) / 247) * 24) + 232)

    def to_ansi_range(a):
        return int(round(a / 51.0))

    r_in_range = to_ansi_range(r)
    g_in_range = to_ansi_range(g)
    b_in_range = to_ansi_range(b)
    xterm_code = int(16 + (36 * r_in_range) + (6 * g_in_range) + b_in_range)  # код xterm-color цвета

    return xterm_code


# inverted = True => белый по черному, False => черный по белому
def brightness_to_ascii(brightness, inverted=False):
    """
    Возвращает ASCII-символ нужной яркости.
    :param brightness: float - яркость кусочка
    :param inverted: bool - инверсия яркости
    :return: str - нужный ASCII-символ
    """
    order = round((brightness if inverted else 1 - brightness) * (len(template) - 1))
    return template[order]


def pixel_is_inside(pixel_coord, row, column):
    """
    Определяет, затрагивает ли кусочек, заданный строкой и столбцом, данный пиксель.
    :param pixel_coord: (int, int) - координаты пикселя
    :param row: выделенная строка с гориз. сечениями = (top, bottom); top, bottom в формате (pix_num, frac_part)
    :param column: выделенный столбец с верт. сечениями = (left, right); left, right в формате (pix_num, frac_part)
    :return: bool - затронут ли пиксель
    """
    x, y = pixel_coord
    left, right = column  # left, bottom, top, left грани в формате (pix_number, fraction)
    top, bottom = row

    if x < left[0] or right[0] < x:
        return False
    if left[1] == 1.0 and left[0] == x:
        return False
    if right[1] == 0 and x == right[0]:
        return False

    if y < top[0] or bottom[0] < y:
        return False
    if top[1] == 1.0 and top[0] == y:
        return False
    if bottom[1] == 0 and y == bottom[0]:
        return False

    return True


def calc_pixel_surface(row, column, pixel_coord):
    """
    Вычисляет затронутую кусочком плоскость пикселя
    :param row: выделенная строка с гориз. сечениями = (top, bottom); top, bottom в формате (pix_num, frac_part)
    :param column: выделенный столбец с верт. сечениями = (left, right); left, right в формате (pix_num, frac_part)
    :param pixel_coord: (int, int) - координаты пикселя
    :return: float - затронутая кусочком плоскость пикселя
    """
    if not pixel_is_inside(pixel_coord, row, column):
        return 0.0
    left, right = column  # left, bottom, top, left грани в формате (pix_coord, fraction)
    top, bottom = row
    x, y = pixel_coord
    upper_edge, left_edge = 0.0, 0.0
    bottom_edge, right_edge = 0.0, 0.0

    if left[0] == x:
        left_edge = left[1]
    elif left[0] < x:
        left_edge = 0.0

    if right[0] == x:
        right_edge = right[1]
    elif right[0] > x:
        right_edge = 1.0

    if top[0] == y:
        upper_edge = top[1]
    elif top[0] < y:
        upper_edge = 0.0

    if bottom[0] == y:
        bottom_edge = bottom[1]
    elif bottom[0] > y:
        bottom_edge = 1.0

    return (right_edge - left_edge) * (bottom_edge - upper_edge)


# имеется в виду яркость пикселя как части куска, яркость которого нужно выровнять
def calc_pixel_brightness(row, column, rgb_img, pixel_coord):  # в шкале 0-255
    """
    Вычисляет яркость пикселя с учётом затронутой плоскости
    :param row: выделенная строка с гориз. сечениями = (top, bottom); top, bottom в формате (pix_num, frac_part)
    :param column: выделенный столбец с верт. сечениями = (left, right); left, right в формате (pix_num, frac_part)
    :param rgb_img: изображение, конвертированное в RGB-сетку
    :param pixel_coord: (int, int) - координаты пикселя
    :return:
    """
    return (rgb_to_brightness(*rgb_img.getpixel(pixel_coord)) *
            calc_pixel_surface(row, column, pixel_coord))


def calc_picture_slices(img_size, str_length: int):
    """
    Высчитывает горизонтальные и вертикальные сечения, по которым надо разбить картинку для конвертации в ASCII-Art.
    :param img_size: (int, int) - размер конвертируемого изображения
    :param str_length: int - ширина ASCII-арта
    """
    width, height = img_size
    art_width, art_height = calc_art_size(str_length, (width, height))
    vertical_cuts, horizontal_cuts = calc_cuts(art_width, width), calc_cuts(art_height, height)
    return vertical_cuts, horizontal_cuts
