import re
from PIL import Image, ImageDraw, ImageFont

FILE_EXT_PATTERN = re.compile(r'.*\.(?P<ext>.*)$')


def get_extension(directory):
    match = FILE_EXT_PATTERN.search(directory)
    if not match:
        return None
    else:
        return match.group('ext')


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


def draw_multiline(text: str, font, image):
    lines = text.split('\n')
    draw_text = ImageDraw.Draw(image)
    char_w, char_h = font.getsize('W')
    for i in range(len(lines)):
        draw_text.text(
            (0, i * char_h),
            lines[i],
            font=font,
            fill='#000000'
        )


def write_png(art: str, output_directory: str):
    ext = get_extension(output_directory)
    # if ext != 'png':
    #     raise Exception('Output filename has invalid extension. Should be \'.png\'.')

    # font = ImageFont.truetype('../fonts/anonymous_pro.tff', size=24)  # '../fonts/Anonymous_Pro.tff'
    font = ImageFont.load_default()
    image = Image.new('RGB', get_image_size(art, font), color='#FFFFFF')
    draw_multiline(art, font, image)

    image.show()
    image.save(output_directory, format=ext)
