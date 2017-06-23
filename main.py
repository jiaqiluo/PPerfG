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
                node_list[idx].set_placed_layer(event["destination"],
                                                layer_idx)
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
        elif event["method"] == "m":
            layer_idx = data["layers"].index(event["origin"]) + 1
            if node_list[idx].get_placed_layer_idx() == -1:
                node_list[idx].set_placed_layer(event["origin"], layer_idx)
            temp = Node(event["dataset"] + " ")
            temp.copy_dataset_info(node_list[idx])
            node_list[idx].set_child(temp)
            node_list[idx].set_direction(1)
            temp.set_parent(node_list[idx])
            temp_layer_idx = data["layers"].index(event["destination"]) + 1
            temp.set_placed_layer(event["destination"], temp_layer_idx)
            node_list.append(temp)
    return node_list


def set_same_layer(node_list):
    """find the nodes at the same layer and save the list to each node

    Arg:
        node_list: the list of all nodes (except the root)
    """
    length = len(node_list)
    for i in range(length):
        for j in range(i, length):
            if node_list[i].get_placed_layer_idx(
            ) == node_list[j].get_placed_layer_idx(
            ) and node_list[i] != node_list[j]:
                node_list[i].set_same_layer_node(node_list[j])
                node_list[j].set_same_layer_node(node_list[i])


def set_radius(node_list, radius_max):
    """for each node, set its radius depending on its data size

    Args:
        node_list: the list of all nodes (except the root)
        radius_max (int): the radius of the circle
    """
    data_size_list = []
    for node in node_list:
        size = node.get_size()
        if size not in data_size_list:
            data_size_list.append(size)
    largerest = max(data_size_list)
    data_size_list.sort()
    data_size_list.reverse()
    # print data_size_list
    for node in node_list:
        data_size = node.get_size()
        if data_size > 0:
            r = radius_max - data_size_list.index(data_size) * 0.5
            node.set_radius(r)
    return


def set_task_coord(canvas, node_list):
    """set the coordinate of the task

    Args:
        node_list: the list of all nodes (except the root)
        canvas: a canvas object
    """
    for node in node_list:
        if node.get_size() == 0:
            coord = canvas.get_layer_coordinate(node.get_name())
            [x, y] = (coord[2] + coord[0]) / 2, coord[1]
            node.set_coord([x, y])
    return


def set_root(root, node_list):
    """connect the root with its children in the node_list

    Args:
        root (Node): the root node which is not in the list
        node_list: the list of all nodes (except the root)
    """
    for node in node_list:
        if node.get_parent() == 0:
            node.set_parent(root)
            root.set_child(node)
            root.set_child(node)
    return


def set_coord(root, node_list):
    """set the coordinate of all nodes

    Args:
        root (Node): the root node which is not in the list
        node_list: the list of all nodes (except the root)
    """
    root.set_temp_coord(0)
    for node in node_list:
        if node.get_radius() > 0:
            node.adjust_x()
    return


def draw_circles(canvas, node_list):
    """draw the circle representing dataset in the canvas

    Args:
        node_list: the list of all nodes (except the root)
        canvas: a canvas object
    """
    for item in node_list:
        [x, y] = item.get_coord()
        if [x, y] != [0, 0] and item.get_size() != 0:
            canvas.create_circle(
                x, y, item.get_radius(), fill=gv.colors[item.get_type()])
            canvas.create_text(x, y, text=item.get_name())
    return


def draw_edges(canvas, node_list):
    """draw edges between nodes

    Args:
        node_list: the list of all nodes (except the root)
        canvas: a canvas object
    """
    for node in node_list:
        edge_list = node.get_edge()
        if edge_list != []:
            for t in edge_list:
                canvas.create_line(t[0][0], t[0][1], t[1][0], t[1][1])
                if t[2] == 1:
                    canvas.create_arrow(t[1][0], t[1][1], 1)
                if t[2] == 2:
                    canvas.create_arrow(t[0][0], t[0][1], 2)
                if t[2] == 3:
                    canvas.create_arrow(t[1][0], t[1][1], 1)
                    canvas.create_arrow(t[0][0], t[0][1], 2)
    return


def main():
    master = Tk()
    master.title("Sample")
    frame = ttk.Frame(master)
    data = get_data("filename: ")

    c = myCanvas(master, width=gv.window_width, height=gv.window_heiht)
    c.draw_layers(data["layers"], gv.layer_height, gv.layer_width)
    c.draw_tasks(data["tasks"], gv.window_width)
    c.grid(column=0, row=0, padx=(0, 0), pady=(0, 0))

    # t1 = c.create_circle(200, 100, 10, fill="green")
    # c.create_circle(400, 550, 10, fill="red")
    # t3 = c.create_line(200, 100 + 10, 400, 550 - 10)

    node_list = parse(data)
    root = Node("root")
    set_root(root, node_list)
    set_same_layer(node_list)
    set_task_coord(c, node_list)
    # root.traverse_display(0)
    set_radius(node_list, gv.radius_max)
    root.set_temp_coord()
    root.adjust_x()
    draw_edges(c, node_list)
    draw_circles(c, node_list)

    # for item in node_list:
    #     item.display()
    frame.grid()
    master.mainloop()


if __name__ == '__main__':
    main()
