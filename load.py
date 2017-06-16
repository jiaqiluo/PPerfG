# this file contains functions for loading and parsing Json file in the
# program.
import os
import re
import json
from pprint import pprint
from tree import Node


def get_filename(prompt):
    """ask for the name of a .json file

    Arg:
        prompt(string): the specific question showing to the user

    Return:
        string: the .json filename
    """
    count = 0
    regex = ".*json"
    while count < 3:
        fn = raw_input(prompt)
        print("input filename is " + fn)
        if (os.path.exists(fn) & bool(re.match(regex, fn))):
            return fn
        print("The file does not exist or not .json file")
        count += 1
    print("Falied 3 times, program ends.")


def read_in(filename):
    """open the target file and read its conetent in

    Arg:
        filename(string): the name of the .json file to be opend

    Return:
        list: a list which contains everything readed from the file
    """
    with open(filename) as data_file:
        data = json.load(data_file)
        return data


def get_data(prompt):
    """returns the content of a .json file

    Arg:
        prompt(string): the specific question showing to the user

    Return:
        list: a list which contains everything readed from the file
    """
    fn = get_filename(prompt)
    if (fn):
        data = read_in(fn)
        return data


def parse(data):
    """parses the input data to buildup the data structure inside the program

    Arg:
        list: a list which contains everything readed from the file
    """
    node_list = []
    # 1. get the name of all nodes
    datasets = data["datasets"].keys()
    for t in data["tasks"]:
        datasets.append(t["name"])
    # 2. create all nodes and save them to node_list
    for item in datasets:
        temp = Node(item)
        node_list.append(temp)
    # 3. get detaied info for tasks
    #    and save them to corresponding node
    layers_length = len(data["layers"])
    for task in data["tasks"]:
        idx = datasets.index(task["name"])
        node_list[idx].set_runtime(task["runtime"])
        node_list[idx].set_collectionTool(task["collectionTool"])
        node_list[idx].set_placed_layer(layers_length - 1)
    # 4. get detaied info for dataset
    #    and save them to corresponding node
    for item in data["datasets"]:
        idx = datasets.index(item)
        node_list[idx].set_size(data["datasets"][item]["size"])
        node_list[idx].set_type(data["datasets"][item]["type"])
    # 5. traverse events to add more details to each node
    for event in data["events"]:
        # get the index of the corresponding node in
        # datasets, which is the same as in node_list
        idx = datasets.index(event["dataset"])
        # set the layer of the node
        # if the method is "read",
        # then the origin is always a layer where the node should be placed
        if event["method"] == "r":
            layer_idx = data["layers"].index(event["origin"])
            node_list[idx].set_placed_layer(layer_idx)
            # the node for destination is its child_node
        # if the method is "write", then the destination is always a layer
        # where the node should be placed
        elif event["method"] == "w":
            layer_idx = data["layers"].index(event["destination"])
            node_list[idx].set_placed_layer(layer_idx)
        # if the method is "read/write", then the origin is always a layer
        # where the node should be placed
        elif event["method"] == "rw":
            layer_idx = data["layers"].index(event["origin"])
            node_list[idx].set_placed_layer(layer_idx)

    for i in node_list:
        print i.display()


if __name__ == '__main__':
    # data = get_data("filename: ")
    data = read_in("sample1.json")
    # for key in data.keys():
    #     pprint(key)

    print "-----------\ntest for parsing"
    parse(data)
