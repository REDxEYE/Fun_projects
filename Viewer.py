import tkinter as tk
from threading import Thread
from time import sleep
from typing import List

from PIL import ImageTk, Image, ImageDraw


class Viewer(Thread):

    def __init__(self, images: List[Image.Image]):
        super().__init__()
        self.images = images
        self.loaded = False
        self.root: tk.Tk = None
        self.tkimages: List[ImageTk.PhotoImage] = []

    def run(self):
        if not self.root:
            self.root = tk.Tk()

        self.loaded = True
        for image in self.images:
            t_image = ImageTk.PhotoImage(image)
            self.tkimages.append(t_image)
            tk.Label(self.root, image=t_image).pack(side=tk.LEFT)
        self.root.mainloop()

    def wait_for_load(self):
        while not self.loaded:
            sleep(0.1)

    def update(self,im=None,im_id = 0):
        if im:
            self.images[im_id] = im
        for tk_image,image in zip(self.tkimages,self.images):
            tk_image.paste(image)

    def quit(self):
        self.root.quit()


if __name__ == '__main__':
    im = Image.new('RGB', (100, 100))
    draw = ImageDraw.ImageDraw(im)
    viewer = Viewer(im)
    viewer.start()
    viewer.wait_for_load()
    draw.text((5, 1), 'TEST')
    viewer.update()
    draw.text((50, 1), 'TEST')
    viewer.update()
    print('t')
    # viewer.quit()
