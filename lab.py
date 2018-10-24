import time
from math import sin

from PerlinLib import perlin
from Viewer import Viewer
from multiprocessing.pool import ThreadPool
from PIL import Image, ImageDraw, ImageEnhance

size = 512
w, h = size, size
im = Image.new('RGB', (w, h))
viewer = Viewer(im)
viewer.start()
viewer.wait_for_load()
cube_size = w // 20
offset = 0
detail = 1
scale = 1 / 50
evol = 0.01
noise_generator = perlin.PerlinNoise()
rgb = False
if rgb:
    noise = noise_generator.get_noise_frame_rgb
    mode = 'RGB'
else:
    noise = noise_generator.get_noise_frame
    mode = 'L'
draw = ImageDraw.ImageDraw(im)
image_array = noise(w, h, evol, scale, detail)
pool = ThreadPool(processes=8)
frame_time = 1 / 60
fps_lock = not False
while True:
    t = time.time()
    noise(w, h, 0, scale, detail,evol,evol*2)
    t_delta = time.time() - t
    if t_delta < frame_time and fps_lock:
        time.sleep(frame_time - t_delta)
        t_delta = time.time() - t
    fps = 1 / t_delta
    # print('FPS:{:.2f} detail:{}\r'.format(fps,detail),end='')
    viewer.root.wm_title('FPS: {:.2f} Noise detail level: {}\r'.format(fps, detail))
    viewer.update(Image.frombytes(mode, (w, h), image_array))

    # scale += 0.0001
    evol += 1
    # draw.rectangle(((x*cube_size+5,y*cube_size+5),(x*cube_size+cube_size-5,y*cube_size+cube_size-5)),fill = 'white')

    # draw.rectangle(((0, 0), (w,h)),fill = 'black')
    # sleep(.1)
