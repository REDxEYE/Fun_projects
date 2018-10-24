import argparse
import math

from pic2console.pic2console import get_terminal_size, Console
from PIL import Image
from pathlib import Path

TERM_SIZE = get_terminal_size()

def color_diff(c1,c2):
    return max(map(lambda a:abs(a[0]-a[1]),zip(c1,c2)))

def pic2ascii(pic, alpha_color=(255, 255, 255), size=TERM_SIZE,tolerance=16):

    path = Path(pic)
    if not path.exists():
        raise Exception('File "{}" does not exist'.format(path.name))
    image = Image.open(path.open('rb'))  # type: Image.Image
    image = image.convert('RGB')
    if len(size) == 1:
        ratio = float(size[0]) / max(image.size)
        new_size = tuple([math.ceil(x*ratio) for x in image.size])
    else:
        ratio = float(size[0]) / max(image.size)
        new_size = tuple([math.ceil(x * ratio) for x in image.size])
        if new_size[1]>size[1]:
            ratio = float(size[1]) / max(image.size)
            new_size = tuple([math.ceil(x * ratio) for x in image.size])
    size = new_size[0], math.ceil(new_size[1] / 2)
    image = image.resize(size, Image.NEAREST)
    # print(size)
    w,h = image.size
    for y in range(h):
        for x in range(w):
            pixel = image.getpixel((x, y))
            if color_diff(pixel,alpha_color)<tolerance:
                Console.rgb_bg_color(' ', (0, 0, 0))
            else:
                Console.rgb_bg_color(' ', pixel)
        Console.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts image to ANSI art.')
    parser.add_argument('image', default=None,
                        help='pic')
    parser.add_argument('--size', nargs='+', type=int, default=TERM_SIZE,
                        help='Size of pic')
    parser.add_argument('--alpha', nargs='+', type=int, default=(255, 255, 255),
                        help='color of alpha')
    parser.add_argument('--tolerance','-t', type=int, default=32,
                        help='color tolerance' )
    args = parser.parse_args()
    Console.clean()
    pic2ascii(args.image, size=args.size, alpha_color=args.alpha,tolerance = args.tolerance)
    # print(args)
