import re
import image_processor
from sys import argv

help_response = '''
ИСПОЛЬЗОВАНИЕ:
    to_ascii.py [-h | --help] [-translate [длина строки] [директория файла ввода] [-f [директория файла вывода]]]
                
    Здесь
        директория файла ввода      Полный путь изображения, которое надо преобразовать.
        директория файла вывода     Полный путь файла, в который нужно вывести изображение. 
        длина строки                Ширина ASCII-изображения в символах.
        
        Параметры:
            -h | --help     Вывод справки о приложении.
            -f              Вывод ASCII-изображения в файл.
            
По умолчанию чем темнее участок на изображении, тем ярче поле для символа.
Итоговое изображение лучше всего смотрится на светлом фоне. На темном оно будет инвертировано.
'''

file_request = re.compile(r'^-translate (?P<length>[0-9]+?) (?P<input_name>.+?) -f (?P<output_name>.+)$')
cli_request = re.compile(r'^-translate (?P<length>[0-9]+?) (?P<input_name>.+?)$')


def run():
    '''
    Запускает приложение из консоли, обрабатывает введённые значения.
    :return: None
    '''
    if len(argv) == 1:
        print('Инструкции не даны.\nЗапустите программу с параметром -h или --help для вызова справки.')
    elif len(argv) == 2:
        if argv[1] == '-h' or argv[1] == '--help':
            print(help_response)
        else:
            print('Некорректный ввод. Для вывода справки запустите скрипт с параметром -h или --help.')
    else:
        query = ' '.join(argv[1:])
        result = file_request.search(query)
        if result:
            art_len = int(result.group(1))
            input_filename = result.group(2)
            output_filename = result.group(3)

            art = image_processor.process(input_filename, art_len, False)
            with open(output_filename, "w") as out_file:
                out_file.write(art)
        else:
            result = cli_request.search(query)
            if result:
                art_len = int(result.group(1))
                input_filename = result.group(2)
                art = image_processor.process(input_filename, art_len, True)
                print(art)
            else:
                print('Некорректный ввод. Для вывода справки запустите скрипт с параметром -h или --help.')


if __name__ == '__main__':
    run()
