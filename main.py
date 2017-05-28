#!/usr/bin/python
from Tkinter import *
import math
from load import *

master = Tk()
master.title("Sample")
# Globle variables
ROW_INDEX = 0
WIDTH = 500
HEIGHT = 0
COLORS = ("yellow", "grey", "white", "cyan", "magenta", "blue", "red")
rows_coord = {}
boxs_coord = {}


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle_arc = _create_circle_arc


# def _create_layout(self, w, h, title, row_num):
#     Label(self, text=title, relief=RIDGE).grid(row=row_num)
#     c = Canvas(self, width=w, height=h)
#     c.grid(row=row_num, column=1)
#     c.create_rectangle(w, h, 3, 3, fill="yellow")
#
#
# Tk.create_layout = _create_layout


def _create_row(self, title, height=100, color="white"):
    global ROW_INDEX, HEIGHT, WIDTH
    self.create_text(60, HEIGHT + height / 2, text=title, anchor=CENTER)
    t = self.create_rectangle(WIDTH, height + HEIGHT,
                              110, HEIGHT + 10, fill=color)
    ROW_INDEX += 1
    HEIGHT += height
    return t


Canvas.create_row = _create_row


def _draw_rows(self, layer_list):
    global rows_coord
    t = 0
    for item in layer_list:
        if(item == "Job Run" or item == "Application"):
            continue
        row = self.create_row(item, 80, COLORS[t % len(COLORS)])
        t += 1
        # print(self.coords(row))
        rows_coord[item] = self.coords(row)


Canvas.draw_rows = _draw_rows


def _draw_tasks(self, task_list):
    global HEIGHT, boxs_coord
    t = 1
    list_len = len(task_list)
    box_width = (WIDTH - 110) / (list_len + 1)
    box_height = box_width - 10
    for item in task_list:
        rightbottom_x = 110 + t * (box_width) + (t - 1) * 10
        rightbottom_y = HEIGHT + 15 + box_height
        lefttop_x = 110 + (t - 1) * box_width + (t - 1) * 10
        lefttop_y = HEIGHT + 15
        rect = self.create_rectangle(
            rightbottom_x, rightbottom_y, lefttop_x, lefttop_y, fill="white")
        t += 1
        boxs_coord[item["name"]] = self.coords(rect)
        self.create_text(lefttop_x, rightbottom_y + 10, text=item["name"], anchor=W)
        self.create_text(lefttop_x, rightbottom_y + 10 +
                         20, text="*human*", anchor=W)
    HEIGHT = rightbottom_y + 10 + 10


Canvas.draw_tasks = _draw_tasks


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


def _draw_circle(self, name, data):
    row = data["createdLayer"]


Canvas.draw_circle = _draw_circle
#  Window
#  |- archive layer
#  |- storage layer
#  |- network
#  |- near storage layer - NVRAM
#  |- memory layer
#  |- job run layer
#  |- notes

if __name__ == '__main__':
    data = get_data("filename: ")
    # pprint(data)
    for key in data.keys():
        pprint(key)

    c1 = Canvas(master, width=WIDTH + 30, height=1000)
    c1.pack()
    c1.draw_rows(data["layers"])
    pprint(rows_coord)

    c1.draw_tasks(data["tasks"])
    pprint(boxs_coord)

    for i in data["datasets"]:
        print i
        # c1.draw_circle(i, data["dataset"][i])

    t1 = c1.create_circle(200, 100, 10, fill="green")
    c1.create_circle(400, 550, 10, fill="red")
    t3 = c1.create_line(200, 100 + 10, 400, 550 - 10)

    master.mainloop()
