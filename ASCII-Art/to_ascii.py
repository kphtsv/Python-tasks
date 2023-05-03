import re
from ascii_converter import image_processor
from sys import argv

with open('help.txt', 'r', encoding='utf-8') as help_file:
    help_response = help_file.read()

INPUT_PATTERN = re.compile(r'^-(?P<output_type>[it]) (?P<length>[0-9]+) (?P<input_dir>.+?) (?P<output_dir>.+)$')
FILE_EXT_PATTERN = re.compile(r'.*\.(?P<ext>.*)$')
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


def get_extension(directory):
    match = FILE_EXT_PATTERN.search(directory)
    if not match:
        return None
    else:
        return match.group('ext')


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
        art_len = int(match.group('length'))
        input_dir = match.group('input_dir')
        output_dir = match.group('output_dir')

        if art_len < 1 or MAX_LENGTH < art_len:
            print('Length value is either too short or too long. Try again.')
            exit(0)

        file_ext = get_extension(input_dir)
        if file_ext == 'jpg' or file_ext == 'png':
            art = image_processor.process(input_dir, art_len, False)

            if output_type == 't':
                with open(output_dir, "w") as out_file:
                    out_file.write(art)
            else:
                pass  # TODO: текст в картинку!
        else:
            print('Unsupported input file extension. Try again with .png or .jpg image.')
            exit(0)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:  # не работает?
        print('Shutting down.')
