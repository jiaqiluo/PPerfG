#!/usr/bin/python
from Tkinter import *
import math
from load import *
from canvasTooltip import *


class MyCanvas(Canvas):
    row_index = 0
    width = 500
    height = 0
    colors = ("yellow", "grey", "white", "cyan", "magenta", "blue", "red")
    rows_coord = {}
    boxs_coord = {}
    tooltips = []

    def create_circle_arc(self, x, y, r, **kwargs):
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)

    def create_row(self, title, height=100, color="white"):
        self.create_text(
            60, self.height + height / 2, text=title, anchor=CENTER)
        t = self.create_rectangle(
            self.width,
            height + self.height,
            110,
            self.height + 10,
            fill=color)
        self.row_index += 1
        self.height += height
        return t

    def draw_rows(self, layer_list):
        t = 0
        for item in layer_list:
            if (item == "Job Run" or item == "Application"):
                continue
            row = self.create_row(item, 80, self.colors[t % len(self.colors)])
            t += 1
            # print(self.coords(row))
            self.rows_coord[item] = self.coords(row)
        return

    def draw_tasks(self, task_list, human):
        t = 1
        list_len = len(task_list)
        box_width = (self.width - 110) / (list_len + 1)
        box_height = box_width - 10
        for item in task_list:
            # calculate coordinates
            rightbottom_x = 110 + t * (box_width) + (t - 1) * 10
            rightbottom_y = self.height + 15 + box_height
            lefttop_x = 110 + (t - 1) * box_width + (t - 1) * 10
            lefttop_y = self.height + 15
            t += 1
            rect = self.create_rectangle(
                rightbottom_x,
                rightbottom_y,
                lefttop_x,
                lefttop_y,
                fill="white",
                activefill="yellow",
                tags=("rectangle", t))
            self.boxs_coord[item["name"]] = self.coords(rect)
            self.create_text(
                lefttop_x, rightbottom_y + 10, text=item["name"], anchor=W)
            if (item["name"] in human):
                self.create_text(
                    lefttop_x,
                    rightbottom_y + 10 + 20,
                    text="*human*",
                    anchor=W)
            info = "name: " + str(item["name"]) + "\nruntime: " + str(item["runtime"]) + "\ncollectionTool: " + str(item["collectionTool"])
            tooltip = CanvasTooltip(self, rect, text=info)
        self.height = rightbottom_y + 10 + 10
        self.tooltips.append(tooltip)
        return

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def draw_circle(self, name, data):
        row = data["createdLayer"]

    def onClick(self, event):
        coords = self.canvasx(event.x, 1), self.canvasy(event.y, 1)
        found = self.find_closest(*coords)[0]
        if found:
            self.target = found
            self.drag_x, self.drag_y = coords
            self.tag_raise(found)
        else:
            self.target, self.drag_x, self.drag_y = None, None, None

    def onDrag(self, event):
        if self.target is None:
            return
        coords = self.canvasx(event.x, 1), self.canvasy(event.y, 1)
        self.move(self.target, coords[0] - self.drag_x,
                  coords[1] - self.drag_y)
        self.drag_x, self.drag_y = coords

    def onRelease(self, event):
        self.target, self.drag_x, self.drag_y = None, None, None


if __name__ == '__main__':
    master = Tk()
    master.title("Sample")
    frame = ttk.Frame(master)
    data = get_data("filename: ")

    for key in data.keys():
        pprint(key)

    c = frame.canvas = MyCanvas(master, width=530, height=1000)
    # c.pack()
    c.draw_rows(data["layers"])
    c.draw_tasks(data["tasks"], data["human"])
    c.tag_bind('rectangle', '<Button-1>', c.onClick)
    c.tag_bind('rectangle', '<B1-Motion>', c.onDrag)
    c.tag_bind('rectangle', '<ButtonRelease-1>', c.onRelease)
    c.grid(column=0, row=0, padx=(0, 0), pady=(0, 0))
    for i in data["datasets"]:
        print i
        # c1.draw_circle(i, data["dataset"][i])

    t1 = c.create_circle(200, 100, 10, fill="green")
    c.create_circle(400, 550, 10, fill="red")
    t3 = c.create_line(200, 100 + 10, 400, 550 - 10)

    frame.grid()
    master.mainloop()
