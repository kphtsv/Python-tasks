from PIL import Image
import calculator



def flatten_slice(row, column, rgb_img):  # возвр. яркость куска
    '''
    Вычисляет среднюю яркость куска на пересечении строки и столбца.
    :param row: выделенная строка с гориз. сечениями = (top, bottom); top, bottom в формате (pix_num, frac_part)
    :param column: выделенный столбец с верт. сечениями = (left, right); left, right в формате (pix_num, frac_part)
    :param rgb_img: изображение, конвертированное в RGB-сетку
    :return: средняя яркость заданного куска, из [0;1].
    '''
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


def process(filename_in, str_length, inverted):
    '''
    Возваращет ASCII-арт изображения в виде строки.
    :param filename_in: str, полный путь файла ввода
    :param str_length: int, ширина ASCII-арта в кол-ве символов
    :param inverted: bool, инверсия изображения по яркости
    :return: str, ASCII-арт
    '''
    if str_length < 1 or int(str_length) != str_length:
        raise Exception("Incorrect string length input!")

    img = Image.open(filename_in)
    rgb_img = img.convert('RGB')
    width, height = img.size

    art_width, art_height = calculator.calc_art_size(str_length, (width, height))
    vertical_cuts, horizontal_cuts = calculator.calc_cuts(art_width, width), calculator.calc_cuts(art_height, height)

    result_char_list = []
    prev_hc = horizontal_cuts[0]
    for ih in range(1, len(horizontal_cuts)):
        prev_vc = vertical_cuts[0]
        for iv in range(1, len(vertical_cuts)):
            row = (prev_hc, horizontal_cuts[ih])
            column = (prev_vc, vertical_cuts[iv])
            slice_brightness = flatten_slice(row, column, rgb_img)
            char = calculator.brightness_to_ascii(slice_brightness, inverted)
            result_char_list.append(char * 1)  # stretching factor
            prev_vc = vertical_cuts[iv]
        result_char_list.append('\n')
        prev_hc = horizontal_cuts[ih]

    return ''.join(result_char_list)
