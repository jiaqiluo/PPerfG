#!/usr/bin/python
from Tkinter import *
import math

master = Tk()
master.title("Sample")
# Globle variables
ROW_INDEX = 0
HEIGHT = 0


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle_arc = _create_circle_arc


def _create_layout(self, w, h, title, row_num):
    Label(self, text=title, relief=RIDGE).grid(row=row_num)
    c = Canvas(self, width=w, height=h)
    c.grid(row=row_num, column=1)
    c.create_rectangle(w, h, 3, 3, fill="yellow")


Tk.create_layout = _create_layout


def _create_row(self, title, height=100, color="white"):
    global ROW_INDEX, HEIGHT
    self.create_text(60, HEIGHT + height / 2, text=title, anchor=CENTER)
    self.create_rectangle(450, height + HEIGHT, 110, HEIGHT + 10, fill=color)
    ROW_INDEX += 1
    HEIGHT += height


Canvas.create_row = _create_row


#  Window
#  |- archive layer
#  |- storage layer
#  |- network
#  |- near storage layer - NVRAM
#  |- memory layer
#  |- job run layer
#  |- notes

c1 = Canvas(master, width=500, height=1000)
c1.pack()

c1.create_row("archive layer", 100, "yellow")
c1.create_row("storage layer", 80, "white")
c1.create_row("network layer", 20, "green")
c1.create_row(" NVRAM  layer", 90, "grey")
c1.create_row(" memory layer", 100,)

t1 = c1.create_circle(200, 100, 10, fill="green")
c1.create_circle(400, 550, 10, fill="red")
t3 = c1.create_line(200, 100 + 10, 400, 550 - 10)

master.mainloop()
