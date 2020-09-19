import tkinter as tk
import os
from PIL import Image, ImageTk
from random import shuffle

photo = None


def find_biggest_img_res(img_list):
    biggest_w = 0
    biggest_h = 0
    for filename in img_list:
        im = Image.open(filename)
        size = im.size
        if size[0] > biggest_w:
            biggest_w = size[0]
        if size[1] > biggest_h:
            biggest_h = size[1]
    return biggest_w, biggest_h


def get_img_list():
    img_list = []
    dir_name = "images"
    for filename in os.listdir(dir_name):
        img_list.append(f"{dir_name}/{filename}")
    return img_list


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Guess the picture")
        self.img_list = get_img_list()
        biggest_w, biggest_h = find_biggest_img_res(self.img_list)
        self.w = biggest_w
        self.h = biggest_h

        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h)
        self.canvas.grid(row=0, column=0)

        self.text_place = tk.Canvas(self.root, width=self.w, height=30)
        self.text_place.grid(row=1, column=0)

        self.text_shown = None
        self.next_img = None
        self.isimg = True

        self.display_img()
        self.root.bind_all("<Button-1>", self.left_click)

        tk.mainloop()

    def left_click(self, event):
        if self.isimg:
            self.display_img()
        else:
            self.display_text()

    def display_text(self):
        self.isimg = True
        text = self.next_img.split("/")[1:]
        self.text_shown = self.text_place.create_text(self.w/2, 20, text=text, font="Arial 15 bold", fill="white")

    def display_img(self):
        self.isimg = False
        if self.text_shown is not None:
            self.text_place.delete(self.text_shown)
            self.text_shown = None

        if len(self.img_list) == 0:
            exit()
        shuffle(self.img_list)
        self.next_img = self.img_list.pop()

        global photo
        img_tmp = Image.open(self.next_img)
        photo = ImageTk.PhotoImage(img_tmp)
        self.cur_img = self.canvas.create_image(self.w/2, self.h/2, image=photo)


if __name__ == '__main__':
    Gui()
