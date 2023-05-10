import numpy
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import ascii_converter.image_processor


def write_txt(art: str, output_directory: str):
    filename, ext = os.path.splitext(output_directory)
    if ext != 'txt':
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
    _, ext = os.path.splitext(output_directory)
    image.save(output_directory, format=ext)


SAVING_FRAMES_PER_SECOND = 20


def cv_to_pil_image(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def pil_to_cv_image(image: Image):
    open_cv_image = numpy.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    return open_cv_image


def video_to_frames(video_full_filename: str):
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


def frames_to_ascii_frames(frames: iter, art_width: int):
    ascii_frames = []
    i = 0
    for frame_cv in frames:
        i += 1
        frame_pil = Image.fromarray(cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB))  # cv2 -> PIL.Image
        frame_art = ascii_converter.image_processor.image_to_art(frame_pil, art_width)
        ascii_frame = pil_to_cv_image(write_art_to_image(frame_art))
        ascii_frames.append(ascii_frame)

    return ascii_frames


def frames_to_video(frames: iter, out_filename):
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


def video_to_ascii(full_video_filename: str, art_width: int):
    frames = video_to_frames(full_video_filename)
    ascii_frames = frames_to_ascii_frames(frames, art_width)
    name = os.path.splitext(os.path.basename(full_video_filename))[0]
    saved_dir = frames_to_video(ascii_frames, name)

    return saved_dir
