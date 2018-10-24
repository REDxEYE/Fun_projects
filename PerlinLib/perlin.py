import time
from ctypes import *
import random
from pathlib import Path


class PerlinNoise:
    path = Path(__file__).absolute().parent / 'PerlinLib.dll'
    lib = windll.LoadLibrary(str(path))
    reseed_generator = lib.reseed_generator
    reseed_generator.argtypes = [c_int]

    generate_noise_frame = lib.generate_noise_frame
    # char* generate_noise_frame(int width, int height, float evolution, float scale, int detail)
    generate_noise_frame.argtypes = [POINTER(c_uint8*1), c_int, c_int, c_float, c_float, c_int,c_float,c_float]

    generate_noise_frame_rgb = lib.generate_noise_frame_rgb
    # char* generate_noise_frame_rgb(int width, int height, float evolution, float scale, int detail)
    generate_noise_frame_rgb.argtypes = [POINTER(c_uint8*1), c_int, c_int, c_float, c_float, c_int,c_float,c_float]

    buffer = bytes()

    def __init__(self, seed=random.randint(0, 65535)):
        self.reseed_generator(seed)

    def get_noise_frame(self, w, h, evol, scale, detail, xoffset=0.0, yoffset=0.0):
        if len(self.buffer) < w * h:
            self.buffer = (c_uint8 * (w * h))()
            old = self.generate_noise_frame.argtypes
            old[0] = POINTER(ARRAY(c_uint8, w * h))
            self.generate_noise_frame.argtypes = old
        self.generate_noise_frame(byref(self.buffer), w, h, evol, scale, detail,xoffset,yoffset)
        return self.buffer

    def get_noise_frame_rgb(self, w, h, evol, scale, detail, xoffset=0.0, yoffset=0.0):
        if len(self.buffer) < w * h:
            self.buffer = (c_uint8 * (w * 3 * h))()
            old = self.generate_noise_frame.argtypes
            old[0] = POINTER(ARRAY(c_uint8, w * h*3))
            self.generate_noise_frame.argtypes = old
        self.generate_noise_frame_rgb(byref(self.buffer), w, h, evol, scale, detail,xoffset,yoffset)
        return self.buffer


if __name__ == '__main__':
    a = PerlinNoise()
    t = time.time()
    b = a.get_noise_frame(512, 512, 0.1, 1, 10)
    print('Took {}ms'.format((time.time() - t) * 1000))
