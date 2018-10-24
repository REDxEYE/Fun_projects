from time import sleep, time

import Viewer
from PIL import Image, ImageDraw
from math import *

from ConstantTime import GameClock


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.x, self.y

    def draw(self, canvas: ImageDraw.ImageDraw):
        canvas.point(self.tuple, 'black')


g = 9.81
pi2 = pi * 2


class Pendulum:

    def __init__(self, length=30.0, mass=2.0, angle=2.0, velocity=0.0, acc=0.0, damping=0.999):
        self.start = Point(0, 0)
        self.length = length
        self._mass = mass
        self._angle = radians(angle)
        self.velocity = velocity
        self.damping = damping
        self.acc = acc
        self.child = None  # type:Pendulum
        self.parent = None  # type:Pendulum

    @property
    def angle(self):
        return degrees(self._angle)

    def __repr__(self):
        return '<Pendulum angle:{:.2f} mass:{} acceleration:{:.2f} velocity:{:.2f}>'.format(self.angle, self.mass,
                                                                                            self.acc, self.velocity)

    @angle.setter
    def angle(self, value):
        self._angle = radians(value)

    @property
    def mass(self):
        if self.child and False:
            return self._mass + self.child.mass * abs(cos(self.child._angle))
        else:
            return self._mass

    def update(self,delta):
        if self.child:

            m1 = self.mass
            m2 = self.child.mass
            a1 = self._angle
            a2 = self.child._angle
            r1 = self.length
            r2 = self.child.length
            a1_v = self.velocity
            a2_v = self.child.velocity
            num1 = -g * (2 * m1 + m2) * sin(a1)
            num2 = -m2 * g * sin(a1 - 2 * a2)
            num3 = -2 * sin(a1 - a2) * m2
            num4 = a2_v * a2_v * r2 + a1_v * a1_v * r1 * cos(a1 - a2)
            den = r1 * (2 * m1 + m2 - m2 * cos(2 * a1 - 2 * a2))
            self.acc = (num1 + num2 + num3 * num4) / den
            self.child.update(delta)


        else:
            m1 = self.parent.mass
            m2 = self.mass
            a1 = self.parent._angle
            a2 = self._angle
            r1 = self.parent.length
            r2 = self.length
            a1_v = self.parent.velocity
            a2_v = self.velocity
            num1 = 2 * sin(a1 - a2)
            num2 = (a1_v * a1_v * r1 * (m1 + m2))
            num3 = g * (m1 + m2) * cos(a1)
            num4 = a2_v * a2_v * r2 * m2 * cos(a1 - a2)
            den = r2 * (2 * m1 + m2 - m2 * cos(2 * a1 - 2 * a2))
            self.acc = (num1 * (num2 + num3 + num4)) / den


        if self._angle >= pi2:
            self._angle -= floor(self._angle / pi2) * pi2
        elif self._angle <= -pi2:
            self._angle += abs(floor(self._angle / pi2)) * pi2
        self.velocity += self.acc*delta
        self._angle += self.velocity
        self.velocity *= self.damping
        if self.child:
            self.child.start = self.end_point

    def draw(self, canvas: ImageDraw.ImageDraw):
        canvas.line((self.start.tuple, self.end_point.tuple), 'black')
        x, y = self.end_point.tuple
        canvas.ellipse((x - 5, y - 5, x + 5, y + 5), 'black')
        if self.child:
            self.child.draw(canvas)

    @property
    def end_point(self):
        x = self.start.x + self.length * sin(self._angle)
        y = self.start.y + self.length * cos(self._angle)
        return Point(x, y)

    @property
    def last(self):
        if self.child:
            return self.child.last
        else:
            return self

    def append(self, other: 'Pendulum'):
        self.child = other
        other.start = self.end_point
        other.parent = self


prev_point = None


def draw(fps):
    global prev_point
    if prev_point:
        canvas_lines.line((a.last.end_point.tuple, prev_point.tuple), fill='black', width=0)
    a.draw(canvas)
    viewer.root.wm_title('FPS: {:.2f}\r'.format(fps))
    canvas.multiline_text((20, 20), "A1:{}\nA2:{}".format(a, a2), fill='black')
    viewer.update()
    canvas.rectangle(((0, 0), im.size), 'white')
    prev_point = a.last.end_point


if __name__ == '__main__':
    frame_time = 1 / 60
    im = Image.new('RGB', (800, 800), (255, 255, 255))
    lines = Image.new('RGB', (800, 800), (255, 255, 255))
    viewer = Viewer.Viewer([im, lines])
    # viewer = Viewer.Viewer([im])
    viewer.start()
    viewer.wait_for_load()
    canvas = ImageDraw.ImageDraw(im)
    canvas_lines = ImageDraw.ImageDraw(lines)
    # a = Pendulum(angle=0, length=100, mass=10, damping=0.999)
    a = Pendulum(angle=degrees(pi / 2), length=100, mass=40, damping=1)
    a.start = Point(im.size[0] // 2, im.size[1] // 2)
    # a2 = Pendulum(angle=0, length=100, mass=10, damping=0.999)
    a2 = Pendulum(angle=degrees(pi / 2), length=100, mass=40, damping=1)
    # a3 = Pendulum(angle=degrees(pi / 2), length=100, mass=40, damping=1)
    # a4 = Pendulum(angle=degrees(pi / 4), length=50, mass=10, damping=0.999)
    a.append(a2)
    # a2.append(a3)
    # a3.append(a4)
    t = time()
    t_delta = 0
    while 1:
        if t_delta <= 0:
            t_delta = frame_time
        a.update(t_delta)
        draw(1 / t_delta)
        t_delta = time() - t

        t = time()
