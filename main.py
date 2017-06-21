#!/usr/bin/python
from Tkinter import *
import math

from load import *
from canvasTooltip import *
from myCanvas import myCanvas
import globalVariables as gv


def parse(data):
    """parses the input data to buildup the data structure inside the program

    Arg:
        data: a list which contains everything readed from the file

    Return:
        node_list (list of Node): all nodes in the tree
    """
    node_list = []
    # 1. get the name of all nodes
    name_list = data["datasets"].keys()
    for t in data["tasks"]:
        name_list.append(t["name"])
    # 2. create all nodes and save them to node_list
    # note: here the order of node in the node_list is the same as the
    # order in the datasets, and we will take advantage of this fact in
    # the following design and development
    for item in name_list:
        temp = Node(item)
        node_list.append(temp)
    # 3. get detaied info for tasks
    #    and save them to corresponding node
    layers_length = len(data["layers"])
    for task in data["tasks"]:
        idx = name_list.index(task["name"])
        node_list[idx].set_runtime(task["runtime"])
        node_list[idx].set_collectionTool(task["collectionTool"])
        node_list[idx].set_placed_layer(task["name"], layers_length)
    # 4. get detaied info for dataset
    #    and save them to corresponding node
    for item in data["datasets"]:
        idx = name_list.index(item)
        node_list[idx].set_size(data["datasets"][item]["size"])
        node_list[idx].set_type(data["datasets"][item]["type"])
    # 5. traverse events to add more details to each node
    for event in data["events"]:
        # get the index of the corresponding node in
        # datasets, which is the same as in node_list
        idx = name_list.index(event["dataset"])
        # set the layer of the node, if the method is "read",
        # then the origin is the layer where the node should be placed
        if event["method"] == "r":
            layer_idx = data["layers"].index(event["origin"]) + 1
            if node_list[idx].get_placed_layer_idx() == -1:
                node_list[idx].set_placed_layer(event["origin"], layer_idx)
            # the node for destination is its child_node
            child_idx = name_list.index(event["destination"])
            node_list[idx].set_child(node_list[child_idx])
            node_list[idx].set_direction(1)
            node_list[child_idx].set_parent(node_list[idx])
        # if the method is "write", then the destination is always a layer
        # where the node should be placed
        elif event["method"] == "w":
            layer_idx = data["layers"].index(event["destination"]) + 1
            if node_list[idx].get_placed_layer_idx() == -1:
                node_list[idx].set_placed_layer(event["destination"], layer_idx)
            # the node for destination is its child_node
            child_idx = name_list.index(event["origin"])
            node_list[idx].set_child(node_list[child_idx])
            node_list[idx].set_direction(2)
            node_list[child_idx].set_parent(node_list[idx])
        # if the method is "read/write", then the origin is always a layer
        # where the node should be placed
        elif event["method"] == "rw":
            layer_idx = data["layers"].index(event["origin"]) + 1
            if node_list[idx].get_placed_layer_idx() == -1:
                node_list[idx].set_placed_layer(event["origin"], layer_idx)
            # the node for destination is its child_node
            child_idx = name_list.index(event["destination"])
            node_list[idx].set_child(node_list[child_idx])
            node_list[idx].set_direction(3)
            node_list[child_idx].set_parent(node_list[idx])
    return node_list


#
# def set_radius(canvas, node_list, radius_max):
#     data_size_list = []
#     for node in node_list:
#         data_size_list.append(node.get_size())
#     largerest = max(data_size_list)
#     data_size_list.sort()
#     data_size_list.reverse()
#     for node in node_list:
#         data_size = node.get_size()
#         if data_size > 0:
#             r = radius_max - data_size_list.index(data_size) * 0.5
#             node.set_radius(r)
#     return
#
#
def set_task_coord(canvas, node_list):
    for node in node_list:
        if node.get_size() == 0:
            coord = canvas.get_layer_coordinate(node.get_name())
            [x, y] = (coord[2] + coord[0]) / 2, coord[1]
            node.set_coord([x, y])
    return


#
#
# def set_node_coordinate(canvas, node_list):
#     # 1. set all tasks first
#     for node in node_list:
#         if node.get_size() == 0:
#             set_task_coord(canvas, node)
#     # 2. set all circrls then
#     boundary = {}
#     for node in node_list:
#         if node.get_size() != 0:
#             set_circle_origin(canvas, node, boundary)
#
#
# def set_circle_origin(canvas, node, x_boundary):
#     # print node.get_name(),"is on layer: ",node.get_placed_layer(),"Coord: ", canvas.get_layer_coordinate(node.get_placed_layer())
#     placed_layer = node.get_placed_layer()
#     # 1. get the left and bound of the x-coordinate of available area
#     if placed_layer not in x_boundary.keys():
#         layer_coord = canvas.get_layer_coordinate(placed_layer)
#         x_boundary[placed_layer] = layer_coord
#         temp_left_most = layer_coord[0]
#     else:
#         temp_left_most = left_most_x[placed_layer][0]
#     # 2. get the right bound of x-coordinate of available area
#     temp_right_most = left_most_x[placed_layer][2]
#     # 3. get the upper bound
#     temp_up_most = left_most_x[placed_layer][1]
#     temp_down_most = left_most_x[placed_layer][3]


def set_root(root, node_list):
    for node in node_list:
        if node.get_parent() == 0:
            node.set_parent(root)
            root.set_child(node)
    return


def main():
    master = Tk()
    master.title("Sample")
    frame = ttk.Frame(master)
    data = get_data("filename: ")

    width = 500
    height = 600
    c = myCanvas(master, width=gv.window_width, height=gv.window_heiht)
    # c.pack()
    c.draw_layers(data["layers"], gv.layer_height, gv.layer_width)
    c.draw_tasks(data["tasks"], gv.window_width)
    # c.tag_bind('rectangle', '<Button-1>', c.onClick)
    # c.tag_bind('rectangle', '<B1-Motion>', c.onDrag)
    # c.tag_bind('rectangle', '<ButtonRelease-1>', c.onRelease)
    c.grid(column=0, row=0, padx=(0, 0), pady=(0, 0))

    t1 = c.create_circle(200, 100, 10, fill="green")
    c.create_circle(400, 550, 10, fill="red")
    t3 = c.create_line(200, 100 + 10, 400, 550 - 10)

    node_list = parse(data)
    root = Node("root")
    set_root(root, node_list)
    set_task_coord(c, node_list)
    root.traverse_display(0)
    root.get_scope(0)
    # for item in node_list:
    #     item.display()
    frame.grid()
    master.mainloop()


if __name__ == '__main__':
    main()
