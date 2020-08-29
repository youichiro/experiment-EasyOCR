from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import easyocr
import os


FONT_PATH = '/Library/Fonts/AppleGothic.ttf'
LINE_WIDTH = 6
FONT_SIZE = 30


def tuple_lists(xy_list):
    return tuple([tuple(xy) for xy in xy_list])


def get_top_left_xy(xy_list):
    top_left_xt_index = np.array([x + y for x, y in xy_list]).argmin()
    return xy_list[top_left_xt_index]


def make_filename(file_path, suffix):
    return '.'.join(file_path.split('/')[-1].split('.')[:-1]) + suffix


def open_im(image_path, out_dir):
    if (image_path[-3:] in ['png', 'PNG']):
        png_im = Image.open(image_path)
        png_im.load()
        im = Image.new('RGB', png_im.size, (255, 255, 255))
        im.paste(png_im, mask=png_im.split()[3])
    else:
        im = Image.open(image_path)
    origin_im = im.copy()
    detect_im = im.copy()
    text_im = im.copy()
    del im

    output_file = os.path.join(out_dir, make_filename(image_path, '.original.jpg'))
    origin_im.save(output_file, quality=95)
    print('saved ' + output_file)

    return origin_im, detect_im, text_im


def draw_detect(detect_im, results, image_path, out_dir):
    draw = ImageDraw.Draw(detect_im)
    for result in results:
        draw.line(tuple_lists(result[0] + [result[0][0]]), fill='red', width=LINE_WIDTH)

    output_file = os.path.join(out_dir, make_filename(image_path, '.detect.jpg'))
    detect_im.save(output_file, quality=95)
    print('saved ' + output_file)


def draw_text(text_im, results, image_path, out_dir):
    draw = ImageDraw.Draw(text_im)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    for result in results:
        draw.polygon(tuple_lists(result[0]), fill=(255, 255, 255), outline=(0, 0, 0))
        draw.text(tuple(get_top_left_xy(result[0])), result[1], font=font, fill=(0, 0, 0))

    output_file = os.path.join(out_dir, make_filename(image_path, '.text.jpg'))
    text_im.save(output_file, quality=95)
    print('saved ' + output_file)

    output_file = os.path.join(out_dir, make_filename(image_path, '.text.txt'))
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f"{result[1]}  {result[2]}\n")
    print('saved ' + output_file)



def main():
  reader = easyocr.Reader(['ja','en'])
  parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument('-l', '--lang', nargs='+', required=True, help='languages')
  parser.add_argument('-f', '--file', required=True, help='input image file')
  parser.add_argument('-o', '--out', default='out', help='output directory')
  args = parser.parse_args()

  os.makedirs(args.out, exist_ok=True)

  reader = easyocr.Reader(args.lang, gpu=False)
  print('start')
  results = reader.readtext(args.file)
  origin_im, detect_im, text_im = open_im(args.file, args.out)
  draw_detect(detect_im, results, args.file, args.out)
  draw_text(text_im, results, args.file, args.out)
  print('finish')


if __name__ == "__main__":
    main()
