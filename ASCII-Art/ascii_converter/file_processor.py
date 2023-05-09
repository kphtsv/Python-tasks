import re
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# для обработки видео
from datetime import timedelta
import numpy as np
import os
import cv2


import ascii_converter.image_processor

FILE_EXT_PATTERN = re.compile(r'.*\.(?P<ext>.*)$')


# TODO os.path.splitext(dir)
def get_extension(directory):
    match = FILE_EXT_PATTERN.search(directory)
    if match:
        return match.group('ext')
    else:
        return None


def write_txt(art: str, output_directory: str):
    if get_extension(output_directory) != 'txt':
        raise Exception('Output filename has invalid extension. Should be \'.txt\'.')

    with open(output_directory, 'w', encoding='utf-8') as out_file:
        out_file.write(art)


def get_image_size(art: str, font):
    width = art.find('\n')
    height = int((len(art)) / (width + 1))
    char_w, char_h = font.getsize('W')
    return width * char_w, height * char_h


def write_art_to_image(art: str):
    font = ImageFont.load_default()
    image = Image.new('RGB', get_image_size(art, font), color='#FFFFFF')

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


def save_image(image: Image, output_directory: str):
    ext = get_extension(output_directory)
    image.save(output_directory, format=ext)


SAVING_FRAMES_PER_SECOND = 10


def format_timedelta(td):  # td == timedelta
    result = str(td)
    try:
        result, ms = result.split('.')
    except ValueError:
        return result + '.00'.replace(':', '-')

    ms = round(int(ms) / 10000)
    return f'{result}.{ms:02}'.replace(':', '-')


def save_video_frames(video_filename: str):
    video_clip = VideoFileClip(video_filename)
    filename, _ = os.path.splitext(video_filename)

    if not os.path.isdir(filename):
        os.mkdir(filename)

    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second

    for current_duration in np.arange(0, video_clip.duration, step):
        frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration)).replace(':', '-')
        frame_filename = os.path.join(filename, f'frame-{frame_duration_formatted}.jpg')
        video_clip.save_frame(frame_filename, current_duration)
    return filename


def video_to_ascii_frames(video_filename: str, art_length: int):
    frames_folder = save_video_frames(video_filename)
    frame_list = [os.path.join(frames_folder, name) for name in os.listdir(frames_folder)]  # 'videos\bad_apple\frame-_.jpg'

    processed_frames_folder = os.path.join(frames_folder + '_processed')
    if not os.path.isdir(processed_frames_folder):
        os.mkdir(processed_frames_folder)

    for frame_dir in frame_list:
        frame_name, ext = os.path.splitext(os.path.basename(frame_dir))
        art = ascii_converter.image_processor.process(frame_dir, art_length, False)
        output_directory = os.path.join(processed_frames_folder, frame_name + '.png')

        img = write_art_to_image(art)
        save_image(img, output_directory)


# def get_video_frames(video_filename: str):
#     video_clip = VideoFileClip(video_filename)
#     frames = [Image.fromarray(video_clip.get_frame(1))]
#     return frames


def frame_sequence_to_video(frames_folder: str):
    frame_duration = 1 / 10  # 10 кадров в секунду
    frame_list = [os.path.join(frames_folder, name) for name in os.listdir(frames_folder)]  # 'videos\bad_apple\frame-_.jpg'
    output_name = os.path.join(frames_folder, 'video.mp4')  # пишет в папку с фреймами

    clip = ImageSequenceClip(frame_list, fps=10)
    clip.write_videofile(output_name)

    return output_name


# https://ru.stackoverflow.com/questions/1446982/python-сгенерировать-5-ти-секундное-mp4-видео-из-одного-фото
# быстрое решение, но с cv2.

# медленное, но рабочее решение
def video_to_ascii(video_filename: str, art_length: int):
    frames_dir = save_video_frames(video_filename)
    location = frame_sequence_to_video(frames_dir)


    print(f'Video is located at: {location}')
