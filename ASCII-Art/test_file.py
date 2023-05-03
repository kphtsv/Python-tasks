import ascii_converter.file_processor
import ascii_converter.image_processor


def run():
    # ascii_converter.file_processor.write_png('vv``\n++vv\nvvff\nccvv\nvvbb\n$$vv\n', '../images/result.png')
    art = ascii_converter.image_processor.process('images/aa.png', 150, False)
    ascii_converter.file_processor.write_png(art, 'images/result.png')
