from ascii_converter import image_processor, file_processor
from sys import argv
import os
import re
import argparse

# with open('help.txt', 'r', encoding='utf-8') as help_file:
#     help_response = help_file.read()

INPUT_PATTERN = re.compile(r'^-(?P<output_type>[itv]) -(?P<is_colored>[mc]) (?P<length>[0-9]+) (?P<input_dir>.+?) '
                           r'(?P<output_dir>.+)$')
MAX_LENGTH = 160

ANSWER_CODE_ANNOTATION = {
    0: 'Некорректный ввод. Для вывода справки запустите скрипт с параметром -h или --help.',
    1: 'Инструкции не даны.\nЗапустите программу с параметром -h или --help для вызова справки.',
    2: 'Вызов --help.',
    3: 'Запрос корректен.'
}


def arg_parse():
    """
    Обработка аргументов ввода.
    :return: (code: int, data: MatchObject) - код запроса, данные из запроса
    """
    if len(argv) == 1:
        return 1, None
    elif len(argv) == 2 and (argv[1] == '-h' or argv[1] == '--help'):
        return 2, None
    else:
        cli_input = ' '.join(argv[1:]).strip()
        match = INPUT_PATTERN.search(cli_input)
        if match:
            return 3, match
        else:
            return 0, None


def parse_params():
    parser = argparse.ArgumentParser(
        prog='ASCII-конвертер',
        description='Преобразует картинки и видео в ASCII- или ANSI-арт.',
        epilog='По умолчанию чем темнее участок на изображении, тем ярче поле для символа.\n'
               'Итоговое изображение лучше всего смотрится на светлом фоне. На темном оно будет инвертировано.\n'
               'Обратите внимание, что максимальное допустимое значение ширины ASCII-изображения равно 160.'
    )

    parser.add_argument('type', choices=['i', 't', 'v'], type=str, help='Output type: (i)mage, (t)ext, (v)ideo')
    parser.add_argument('mode', choices=['c', 'm'], type=str, help='Color mode: (c)oloed, (m)onochrome')
    parser.add_argument('art_width', help='Ширина ASCII-изображения в символах.', type=int)
    parser.add_argument('input_dir', help='Полный путь файла, которое надо преобразовать.', type=str)
    parser.add_argument('output_dir', help='Полный путь файла, в который нужно вывести изображение или видео.',
                        type=str)

    return parser.parse_args()


def run():
    """
    Запускает приложение из консоли, обрабатывает введённые значения.
    :return: None
    """
    args = parse_params()

    output_type = args.type
    is_colored = True if args.mode == 'c' else False
    art_len = args.art_width
    input_dir = args.input_dir
    output_dir = args.output_dir

    if art_len < 1 or MAX_LENGTH < art_len:
        raise Exception(f'Значение ширины арта либо слишком мало, либо слишком велико (больше {MAX_LENGTH}).')

    _, file_ext = os.path.splitext(input_dir)
    if file_ext == '.jpg' or file_ext == '.png' or file_ext == '.mp4':
        if output_type == 'v':
            saved_dir = file_processor.video_to_ascii(input_dir, art_len, is_colored)
            print(f'Процесс преобразования завершен. Вы можете найти итоговый файл в \"{saved_dir}\".')
            exit(0)

        if is_colored:
            if output_type == 't':
                print('Запись цветного ASCII-изображения в текстовый файл невозможна.')
                print('Попробуйте запустить программу с ключом -i.')
                exit(0)

            rgb_matrix = image_processor.to_ansi_art_from_file(input_dir, art_len)
            if output_type == 'i':
                image = file_processor.write_color_art_to_image(rgb_matrix)
                file_processor.save_image(image, output_dir)
        else:
            art = image_processor.to_ascii_art_from_file(input_dir, art_len, False)
            if output_type == 't':
                file_processor.write_txt(art, output_dir)
            elif output_type == 'i':
                image = file_processor.write_art_to_image(art)
                file_processor.save_image(image, output_dir)
    else:
        raise Exception('Неподдерживаемый формат входных данных. Попробуйте снова с расширениями .png, .jpg или.mp4.')


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Shutting down.')
