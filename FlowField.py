import random
import time
from math import *
from typing import Union

from PIL import Image, ImageDraw, ImageColor
from PerlinLib.perlin import PerlinNoise
from Viewer import Viewer


def random_vector(scale=1):
    return Vector(random.random() * scale, random.random() * scale)


class Vector:

    def __init__(self, x, y):
        self.x, self.y = x, y

    @property
    def tuple(self):
        return self.x, self.y

    def __repr__(self):
        return '<Vector X:{} Y:{}>'.format(self.x, self.y)

    def __imul__(self, other: Union['Vector', int, float]):
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __mul__(self, other: Union['Vector', int, float]):
        if isinstance(other, Vector):
            x = other.x * self.x
            y = other.y * self.y
        else:
            x = other * self.x
            y = other * self.y
        return Vector(x, y)

    def __iadd__(self, other: Union['Vector', int, float]):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self


class Particle:

    def __init__(self, max_speed=1):
        self.max_speed = max_speed
        self.pos = random_vector()
        self.acc = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.prev = self.pos

    def __repr__(self):
        return '<Particle pos:{} vel:{}>'.format(self.pos, self.vel)

    def clamp(self):
        update = False
        if self.pos.x < 0:
            self.pos.x = 1
            update = True
        if self.pos.x > 1:
            self.pos.x = 0
            update = True
        if self.pos.y < 0:
            self.pos.y = 1
            update = True
        if self.pos.y > 1:
            self.pos.y = 0
            update = True
        if self.vel.x > self.max_speed:
            self.vel.x = self.max_speed
        if self.vel.y > self.max_speed:
            self.vel.y = self.max_speed
        if update:
            self.prev = self.pos * 1

    def update(self):
        self.pos += self.vel
        self.vel += self.acc
        self.acc *= 0

    def apply_force(self, force_vec: Vector):
        self.vel += force_vec

    def draw(self, image: Image.Image, canvas: ImageDraw.ImageDraw, size):
        self.clamp()
        x, y = map(lambda c :floor(c), (self.pos * size).tuple) # TODO: ограничить значение

        px, py = map(floor, (self.prev * size).tuple)
        color = ImageColor.getrgb('hsv({},100%,100%)'.format(abs(atan2(*self.vel.tuple) * 2) * 360))
        old_color = image.getpixel((x-1, y-1))
        new_color = [0] * 3
        new_color[0] = int(old_color[0] + color[0] * 0.1)
        new_color[1] = int(old_color[1] + color[1] * 0.1)
        new_color[2] = int(old_color[2] + color[2] * 0.1)
        # canvas.point((x, y), tuple(new_color))
        canvas.line(((px - 1, py - 1), (x - 1, y - 1)), tuple(new_color))
        # image.putpixel((x - 1, y - 1), tuple(new_color))
        # canvas.point((self.pos * size).tuple, fill=(255, 255, 255, 255))


size = 64
perlin = PerlinNoise()
scale = 0.05
grid_size = 10

im = Image.new('RGB', (size * grid_size, size * grid_size), 'black')
canvas = ImageDraw.ImageDraw(im)
viewer = Viewer([im])
viewer.start()
viewer.wait_for_load()
particles = [Particle(random.randint(2, 8)) for _ in range(1000)]
force_grid = [[(0, 0) for _ in range(size)] for _ in range(size)]
z = 0
t = time.time()
t_delta = 0
while 1:
    t = time.time()
    flow_field = perlin.get_noise_frame(size, size, z, scale, 6)
    for index in range(len(flow_field)):
        angle = (flow_field[index] / 255) * pi * 4
        x = int(floor(index / size))
        y = int(floor(index % size))
        force_grid[x][y] = (cos(angle), sin(angle))
        fx, fy = (cos(angle), sin(angle))
        # gx = x*grid_size
        # gy = y*grid_size
        # canvas.line((gx, gy, gx + fx * grid_size, gy + fy * grid_size))
    # im.paste(Image.frombytes('L',(size,size),flow_field))
    for particle in particles:
        particle.clamp()
        px, py = particle.pos.tuple
        flow_vec = Vector(*force_grid[int(ceil(px * size) - 1)][int(ceil(py * size) - 1)]) * 0.0001
        particle.update()
        particle.apply_force(flow_vec)
        particle.draw(im, canvas, size * grid_size)
    viewer.update()
    z += 0.001
    t_delta = time.time() - t
    fps = 1 / t_delta
    viewer.root.wm_title('FPS: {:.2f}'.format(fps))
    # canvas.rectangle(((0, 0), im.size), 'black')
