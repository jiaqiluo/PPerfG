#!/usr/bin/python
from Tkinter import *
import math
from load import *
from canvasTooltip import *
import globalVariables as gv


class myCanvas(Canvas):
    """this class contains data members and functions for drawing the diagram
       and it inherits class 'Canvas' from Tkinter

    Attributes:
        layer_index (int)  : a local variable
        width (int)      : the width of the diagram window
        height (int)     : the height of the diagram window
        colors (tuple)   : the list of colors used for different data types
        layer_coord (list): a local variable for ...
        boxs_coord (list): a local variable for ...
        tooltips (array) : a local variable for ...
    """
    layer_index = 1
    height = 10
    colors = ("yellow", "grey", "white", "cyan", "magenta", "blue", "red")
    layer_coord = {}
    tooltips = []
    layer_list = []

    def create_circle_arc(self, x, y, r, **kwargs):
        """draws an arc, pieslice, or chord on the canvas.

        Args:
            x (float): x coordinates of the center
            y (float): y coordinates of the center
            r (float): the radius of the circle
            kwargs: other arguments (see Tkinter document for details)

        Return:
            the item id
        """
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)

    def get_info(self):
        print "rows:\n ", self.layer_coord

    def get_layer_coordinate(self, item):
        if item in self.layer_coord.keys():
            return self.layer_coord[item]
        else:
            return 0

    def draw_layer(self, title, height, width, color="white"):
        """draw a layer in the canvas

        Args:
            title (string): the title of the row
            height(int)   : the height of the row, initial value is 100
            color(string) : the background color of the row

        Return:
            the item id
        """
        self.create_text(60, self.height + height/2, text=title, anchor=CENTER)
        upper_left_x = gv.layer_name_width
        upper_left_y = self.height
        bottom_right_x = width
        bottom_right_y = height + self.height
        t = self.create_rectangle(bottom_right_x, bottom_right_y,
                                  upper_left_x, upper_left_y, fill=color)
        self.layer_index += 1
        self.height += height
        self.layer_list.append(t)
        return t

    def draw_layers(self, layer_list, layer_height, layer_width):
        """draw several layers from the top to the bottom

        Arg:
            layer_list (list): a list of names of layers
        """
        i = 0
        for item in layer_list:
            row = self.draw_layer(item, layer_height, layer_width, self.colors[i % len(self.colors)])
            i += 1
            self.layer_coord[item] = self.coords(row)
        return

    def draw_tasks(self, task_list, width):
        """draw tasks in the 'Job Run'(or named differntly) layer

        Arg:
            task_list (list): a list of tasks
        """
        t = 1
        list_len = len(task_list)
        box_width = (width - gv.layer_name_width) / (list_len + 1)
        box_height = box_width - 15
        for item in task_list:
            # calculate coordinates
            rightbottom_x = gv.layer_name_width + t * (box_width) + (t - 1) * 10
            rightbottom_y = self.height + 15 + box_height
            lefttop_x = gv.layer_name_width + (t - 1) * box_width + (t - 1) * 10
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
            self.layer_coord[item["name"]] = self.coords(rect)
            self.create_text(
                lefttop_x, rightbottom_y + 10, text=item["name"], anchor=W)
            info = "name: " + str(item["name"]) + \
                "\nruntime: " + str(item["runtime"]) + \
                "\ncollectionTool: " + str(item["collectionTool"])
            # bind the task object with a callback function
            tooltip = CanvasTooltip(self, rect, text=info)

        self.height = rightbottom_y + 10 + 10
        self.tooltips.append(tooltip)
        return

    def create_circle(self, x, y, r, **kwargs):
        """draws a circle on the canvas

        Args:
            x (float): x coordinates of the center
            y (float): y coordinates of the center
            r (float): the radius of the circle
            kwargs: other arguments (see Tkinter document for details)

        Return:
            the item id
        """
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
