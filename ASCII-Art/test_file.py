from ascii_converter import *


def run():
    # ascii_converter.file_processor.write_png('vv``\n++vv\nvvff\nccvv\nvvbb\n$$vv\n', '../images/result.png')
    # art = ascii_converter.image_processor.process('images/aa.png', 150, False)
    # ascii_converter.file_processor.write_png(art, 'images/result.png')
    # ascii_converter.file_processor.video_to_ascii_frames('videos\\bad_apple.mp4', 150)
    ascii_converter.file_processor.frame_sequence_to_video('videos\\bad_apple_processed')



run()