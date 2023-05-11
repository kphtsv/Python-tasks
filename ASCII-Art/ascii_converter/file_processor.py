import numpy
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import ascii_converter.image_processor

ANSI_CHARACTERS = ['░', '▒', '▓', '█']


def write_txt(art: str, output_directory: str):
    """
    Пишет заданный текст в файл по директории.
    :param art: str - строка
    :param output_directory: str - директория текстового файла вывода
    """
    filename, ext = os.path.splitext(output_directory)
    if ext != '.txt':
        raise Exception('Output filename has invalid extension. Should be \'.txt\'.')

    with open(output_directory, 'w', encoding='utf-8') as out_file:
        out_file.write(art)


def get_image_size_by_str(art: str, font):
    """
    Возвращает размер кадра с ASCII-артом.
    :param art: str - ASCII-арт
    :param font: шрифт библиотеки Pillow
    :return: (int, int) - размер Pillow-изображения
    """
    width = art.find('\n')
    height = int((len(art)) / (width + 1))
    char_w, char_h = font.getsize('W')
    return width * char_w, height * char_h


def write_art_to_image(art: str):
    """
    Рисует заданный ASCII-Art на картинку.
    :param art: str - ASCII-арт
    :returns: PIL.Image - изображение с нанесённым артом
    """
    font = ImageFont.load_default()
    image = Image.new('RGB', get_image_size_by_str(art, font), color='#FFFFFF')

    lines = art.split('\n')
    draw_text = ImageDraw.Draw(image)
    char_w, char_h = font.getsize('W')
    for i in range(len(lines)):
        draw_text.text(
            (0, i * char_h),
            lines[i],
            font=font,
            fill='#000000'
        )

    return image


def get_image_size_by_matrix(rgb_matrix):
    """
    Возвращает размер кадра с ANSI-артом.
    :param rgb_matrix: list - RGB-матрица ANSI-арта
    :return: (int, int) - размер Pillow-изображения
    """
    height = len(rgb_matrix)
    width = len(rgb_matrix[0])
    char_w, char_h = (16, 29)  # font.getsize('█')
    return width * char_w, height * char_h


def write_color_art_to_image(rgb_matrix):
    """
    Рисует заданный ANSI-Art на картинку.
    :param rgb_matrix: list - RGB-матрица ANSI-арта
    :returns: PIL.Image - изображение с нанесённым артом
    """
    font = ImageFont.truetype(r"C:\WINDOWS\Fonts\Arial.ttf", 25, encoding="utf-8")
    image = Image.new('RGB', get_image_size_by_matrix(rgb_matrix), color='#FFFFFF')
    draw_text = ImageDraw.Draw(image)
    char_w, char_h = 16, 29

    for i in range(len(rgb_matrix)):
        row = rgb_matrix[i]
        for j in range(len(row)):
            r, g, b = rgb_matrix[i][j]

            draw_text.text(
                (j * char_w, i * char_h),
                ANSI_CHARACTERS[-1],
                font=font,
                fill=(r, g, b, 255)  # возможно, здесь BGRA
            )
    return image


def save_image(image: Image, output_directory: str):
    """
    Сохраняет Pillow-изображение по заданной директории.
    :param image: PIL.Image - изображение для сохранения
    :param output_directory: str - директория текстового файла вывода
    """
    _, ext = os.path.splitext(output_directory)
    image.save(output_directory, format=ext[1:])


SAVING_FRAMES_PER_SECOND = 20


def cv_to_pil_image(image):
    """
    Преобразует cv2-изображение в Pillow-изображение.
    :param image: numpy.array - изображение для конвертации
    :returns: PIL.Image - преобразованное изображение
    """
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def pil_to_cv_image(image: Image):
    """
    Преобразует Pillow-изображение в cv2-изображение.
    :param image: PIL.Image - изображение для конвертации
    :returns: numpy.array - преобразованное изображение
    """
    open_cv_image = numpy.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    return open_cv_image


def video_to_frames(video_full_filename: str):
    """
    Извлекает кадры из видео.
    :param video_full_filename: str - директория файла ввода
    :returns: list - список PIL.Image-изображений
    """
    capture = cv2.VideoCapture(video_full_filename)
    fps = capture.get(cv2.CAP_PROP_FPS)
    saving_fps = min(fps, SAVING_FRAMES_PER_SECOND)
    frame_len = fps / saving_fps

    frames = []
    i = 0
    file_count = 0

    while capture.isOpened():
        is_read, frame = capture.read()
        i += 1
        if is_read:
            if i >= frame_len * file_count:
                frames.append(frame)
                file_count += 1
        else:
            break
    capture.release()
    return frames


def frames_to_ascii_frames(frames: iter, art_width: int, is_colored=False):
    """
    Преобразует список кадров в ASCII-кадры.
    :param frames: iter - список PIL.Image-кадров
    :param art_width: int - ширина ASCII-изображения
    :param is_colored: bool - монохром/цвет
    """
    ascii_frames = []
    i = 0
    for frame_cv in frames:
        i += 1
        frame_pil = Image.fromarray(cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB))  # cv2 -> PIL.Image
        if is_colored:
            frame_rgb_matrix = ascii_converter.image_processor.image_to_ansi_art(frame_pil, art_width)
            ascii_frame = pil_to_cv_image(write_color_art_to_image(frame_rgb_matrix))
        else:
            frame_art = ascii_converter.image_processor.image_to_ascii_art(frame_pil, art_width)
            ascii_frame = pil_to_cv_image(write_art_to_image(frame_art))
        ascii_frames.append(ascii_frame)
    return ascii_frames


def frames_to_video(frames: iter, out_filename):
    """
    Склеивает список кадров в видео и сохраняет.
    :param frames: iter - список PIL.Image-кадров
    :param out_filename: str - имя файла вывода
    :return: str - директория сохранённого файла
    """
    if len(frames) == 0:
        raise Exception('Nothing to convert!')

    height, width, _ = frames[0].shape
    frame_size = width, height
    filename = f'videos\\{out_filename}_processed.avi'
    video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc("X", "V", "I", "D"), SAVING_FRAMES_PER_SECOND, frame_size)

    for frame in frames:
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()

    return filename


def video_to_ascii(full_video_filename: str, art_width: int, is_colored=False):
    """
    Выполняет полное преобразование файла видео в файл ASCII- или ANSI-арта.
    :param full_video_filename: str - полное имя видео файла ввода
    :param art_width: int - ширина арта в символах
    :param is_colored: bool - монохром/цвет
    :return: str - директория сохранённого файла
    """
    frames = video_to_frames(full_video_filename)
    ascii_frames = frames_to_ascii_frames(frames, art_width, is_colored)
    name = os.path.splitext(os.path.basename(full_video_filename))[0]
    saved_dir = frames_to_video(ascii_frames, name)

    return saved_dir
