import os
import re
from ascii_converter import image_processor, file_processor
from sys import argv

with open('help.txt', 'r', encoding='utf-8') as help_file:
    help_response = help_file.read()

INPUT_PATTERN = re.compile(r'^-(?P<output_type>[itv]) -(?P<is_colored>[mc]) (?P<length>[0-9]+) (?P<input_dir>.+?) (?P<output_dir>.+)$')
MAX_LENGTH = 300

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


def run():
    """
    Запускает приложение из консоли, обрабатывает введённые значения.
    :return: None
    """
    code, match = arg_parse()
    if code == 0 or code == 1:
        print(ANSWER_CODE_ANNOTATION[code])
    elif code == 2:
        print(help_response)
    else:
        output_type = match.group('output_type')
        is_colored = True if match.group('is_colored') == 'c' else False
        art_len = int(match.group('length'))
        input_dir = match.group('input_dir')
        output_dir = match.group('output_dir')

        if art_len < 1 or MAX_LENGTH < art_len:
            raise Exception('Length value is either too short or too long. Try again.')

        _, file_ext = os.path.splitext(input_dir)
        if file_ext == '.jpg' or file_ext == '.png' or file_ext == '.mp4':
            if output_type == 'v':
                saved_dir = file_processor.video_to_ascii(input_dir, art_len, is_colored)
                print(f'Процесс преобразования завершен. Вы можете найти итоговый файл в \"{saved_dir}\".')
                exit(0)

            if is_colored:
                if output_type == 'i':
                    rgb_matrix = image_processor.to_ansi_art_from_file(input_dir, art_len)
                    image = file_processor.write_color_art_to_image(rgb_matrix)
                    file_processor.save_image(image, output_dir)
                else:
                    print('Запись цветного ASCII-изображения в текстовый файл невозможна.')
                    print('Попробуйте запустить программу с ключом -i.')
            else:
                art = image_processor.to_ascii_art_from_file(input_dir, art_len, False)
                if output_type == 't':
                    file_processor.write_txt(art, output_dir)
                elif output_type == 'i':
                    image = file_processor.write_art_to_image(art)
                    file_processor.save_image(image, output_dir)
        else:
            raise Exception('Unsupported input file extension. Try again with .png or .jpg image.')


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:  # не работает?
        print('Shutting down.')

    # test_file.run()
