from PIL import Image
from ascii_converter import calculator


def flatten_slice_brightness(row, column, rgb_img):
    """
    Вычисляет среднюю яркость куска на пересечении строки и столбца.
    :param row: выделенная строка с гор. сечениями = (top, bottom); top, bottom в формате (pix_num, frac_part)
    :param column: выделенный столбец с вер. сечениями = (left, right); left, right в формате (pix_num, frac_part)
    :param rgb_img: изображение, конвертированное в RGB-сетку
    :return: средняя яркость заданного куска, из [0;1].
    """
    left, right = column  # left, bottom, top, left грани в формате (pix_number, fraction)
    top, bottom = row
    width, height = rgb_img.size

    brightness_sum = 0
    surface_sum = 0
    for hp in range(left[0], right[0] + 1):
        if hp >= width:
            continue
        for vp in range(top[0], bottom[0] + 1):
            if vp >= height:
                continue
            surface = calculator.calc_pixel_surface(row, column, (hp, vp))
            surface_sum += surface
            brightness_sum += calculator.rgb_to_brightness(*(rgb_img.getpixel((hp, vp)))) * surface
    return brightness_sum / surface_sum


def flatten_slice_color(row, column, rgb_img):
    left, right = column  # left, bottom, top, left грани в формате (pix_number, fraction)
    top, bottom = row
    width, height = rgb_img.size

    r_s, g_s, b_s = 0, 0, 0
    surface_sum = 0

    for hp in range(left[0], right[0] + 1):
        if hp >= width:
            continue
        for vp in range(top[0], bottom[0] + 1):
            if vp >= height:
                continue

            surface = calculator.calc_pixel_surface(row, column, (hp, vp))
            surface_sum += surface

            r, g, b = rgb_img.getpixel((hp, vp))
            r_s += r * surface
            g_s += g * surface
            b_s += b * surface

    return round(r_s / surface_sum), round(g_s / surface_sum), round(b_s / surface_sum)


def image_to_ascii_art(img: Image, str_length, inverted=False):
    """
    Возвращает ASCII-арт изображения в виде строки.
    :param img: Image, изображение формата PIL для конвертации
    :param str_length: int, ширина ASCII-арта в кол-ве символов
    :param inverted: bool, инверсия изображения по яркости
    :return: str, ASCII-арт
    """
    if str_length < 1:
        raise Exception("Incorrect string length input!")

    # img = Image.open(filename_in)
    rgb_img = img.convert('RGB')
    vertical_cuts, horizontal_cuts = calculator.calc_picture_slices(img.size, str_length)

    result_char_list = []
    prev_hc = horizontal_cuts[0]
    for ih in range(1, len(horizontal_cuts)):
        prev_vc = vertical_cuts[0]
        for iv in range(1, len(vertical_cuts)):
            row = (prev_hc, horizontal_cuts[ih])
            column = (prev_vc, vertical_cuts[iv])
            slice_brightness = flatten_slice_brightness(row, column, rgb_img)
            char = calculator.brightness_to_ascii(slice_brightness, inverted)
            result_char_list.append(char * 1)  # stretching factor
            prev_vc = vertical_cuts[iv]
        result_char_list.append('\n')
        prev_hc = horizontal_cuts[ih]

    return ''.join(result_char_list)


def to_ascii_art_from_file(filename_in, str_length, inverted=False):
    img = Image.open(filename_in)
    return image_to_ascii_art(img, str_length, inverted)


def image_to_ansi_art(img: Image, str_length):
    if str_length < 1:
        raise Exception("Incorrect string length input!")

    rgb_img = img.convert('RGB')
    vertical_cuts, horizontal_cuts = calculator.calc_picture_slices(img.size, str_length)

    rgb_matrix = []
    prev_hc = horizontal_cuts[0]
    for ih in range(1, len(horizontal_cuts)):
        prev_vc = vertical_cuts[0]
        rgb_row = []
        for iv in range(1, len(vertical_cuts)):
            row = (prev_hc, horizontal_cuts[ih])
            column = (prev_vc, vertical_cuts[iv])
            slice_color = calculator.rgb_to_ansi_color(*flatten_slice_color(row, column, rgb_img))
            rgb_row.append(slice_color)
            prev_vc = vertical_cuts[iv]
        rgb_matrix.append(rgb_row)
        prev_hc = horizontal_cuts[ih]

    return rgb_matrix


def to_ansi_art_from_file(filename_in: str, str_length: int):
    img = Image.open(filename_in)
    return image_to_ansi_art(img, str_length)
