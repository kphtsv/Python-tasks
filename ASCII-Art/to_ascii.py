import image_processor
from sys import argv


def run():
    # python C:\0\Универ\Python-tasks\ASCII-Art\main.py arguments
    # print(argv)
    # script, args = argv
    # print(args)

    if len(argv) == 1:
        print('Инструкции не даны.\nЗапустите программу с параметром -h или --help для вызова справки.')
    if len(argv) == 2:
        if argv[1] == '-h'or argv[1] == '--help':
            help = '''
            ИСПОЛЬЗОВАНИЕ:
                
            '''
            print()


    filename_in = 'C:\\0\\Универ\\Python-tasks\\ASCII-Art\\tests\\TestImages\\small_image_bw.png'
    filename_out = 'tests\\TestImages\\result.txt'
    str_len = 6
    return image_processor.process(filename_in, filename_out, str_len)


if __name__ == '__main__':
    run()