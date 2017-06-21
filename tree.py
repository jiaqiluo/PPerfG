import globalVariables as gv

class Node:
    """This class contains data members and functions of a Node

    Attributes:
        parent (list of Node): the list of parents of the current node
        children (list of Node): the list of children of the current node
        placed_layer (int): the layer of the node in the tree, initial value -1
        name (string): the name of the node
        size (int): the size of the dataset, initial value is 0
        data_type (string): the data type of the dataset
        runtime (int): how long the task runs, intial value is 0
        collectionTool (string): the name of the tool used to collect the data
    """

    def __init__(self, name):
        """the very basic constructor of the class

        Since the node might be either a dataset or a task, so we leave
        setting values to other functions. But 'name' is a must-have attribute
        so we set the name in this basic constructor.

        Arg:
            name (string): the name of the node
        """
        self.name = name
        self.parent = []
        self.children = []
        self.direction = []
        self.layer_name = ""
        self.layer_idx = -1
        self.coordinate = [0, 0]
        # if it is a dataset
        self.size = 0
        self.radius = 0
        self.data_type = ""
        # if it is a task
        self.runtime = 0
        self.collectionTool = ""

    def traverse_display(self, n):
        for i in self.children:
            i.traverse_display(n + 1)
        if len(self.children) == 0:
            print "   " * n, "name:", self.name, "(leaf, coord:", self.get_coord(
            ), ")"
        else:
            print "   " * n, "name: ", self.name
        return

    def get_scope(self, ident):
        x_list = []
        left_most = gv.layer_name_width
        right_most = 0
        for item in self.children:
            temp = item.get_scope(ident+4)
            for t in temp:
                x_list.append(t)
        t = self.coordinate[0]
        if t != 0:
            x_list.append(t)
        x_list.sort()
        print "  " * ident, self.name, x_list
        return x_list




    def display(self):
        """display the content of the current node in a clear format
        """
        print "- - - - - - - - "
        print "name: ", self.name
        print "size: ", self.size
        print "data type: ", self.data_type
        print "layer_name: ", self.layer_name
        print "layer_idx: ", self.layer_idx
        print "runtime: ", self.runtime
        print "collectionTool: ", self.collectionTool
        print "direction: ", self.direction
        print "parent: "
        if self.parent != 0:
            for item in self.parent:
                print " ", item.name
        print "children: "
        for i in range(len(self.children)):
            print self.children[i].get_name()
        return

    def get_name(self):
        """return the name of the current node
        """
        return self.name

    def set_runtime(self, runtime):
        """set the runtime of the current node if it is a task

        Arg:
            rumtime (int): the rumtime of the task
        """
        if runtime != 0:
            self.runtime = runtime
        return

    def set_collectionTool(self, collectionTool):
        """set the collectionTool of the current node if it is a task

        Arg:
            collectionTool (string): the collectionTool of the task
        """
        if collectionTool != "":
            self.collectionTool = collectionTool
        return

    def set_size(self, size):
        """set the size of the current node if it is a dataset

        Arg:
            size (int): the size of the dataset
        """
        if size > 0:
            self.size = size
        return

    def get_size(self):
        return self.size

    def set_type(self, data_type):
        """set the datatype of the current node if it is a dataset

        Arg:
            data_type (string): the datatype of the dataset
        """
        if data_type != "":
            self.data_type = data_type
        return

    def set_parent(self, parent_node):
        """set the parent of the current node

        Arg:
            parent_node (Node): the node representing parent
        """
        if parent_node != 0:
            self.parent.append(parent_node)
        else:
            print("invalid parent node")
        return

    def get_parent(self):
        if len(self.parent) != 0:
            return self.parent
        else:
            return 0

    def set_child(self, child_node):
        """set the child of the current node

        Arg:
           child_node (Node): the node representing child
        """
        if child_node != 0:
            self.children.append(child_node)
        else:
            print("invalid child node")
        return

    def set_placed_layer(self, name, idx):
        """set the placed_layer of the current node

        Arg:
            placed_layer (int): the layer the current node placed in the tree
        """
        self.layer_name = name
        self.layer_idx = idx
        return

    def get_placed_layer_name(self):
        """return the layer numer
        """
        return self.layer_name

    def get_placed_layer_idx(self):
        """return the layer index
        """
        return self.layer_idx

    def set_direction(self, mode=0):
        """set the direction of the arrow line between the node and its children

        Arg:
            mode (int): 0 - no direction;
                        1 - from the current node to child;
                        2 - from child to the current node
                        3 - two-drection arrow
        """
        if mode in [0, 1, 2, 3]:
            self.direction.append(mode)
        else:
            print("invalid mode value")
        return

    def set_radius(self, radius):
        if radius != 0:
            self.radius = radius
        return

    def get_radius(self):
        return self.radius

    def set_coord(self, coord):
        self.coordinate = coord
        return

    def get_coord(self):
        return self.coordinate


if __name__ == '__main__':
    t = Node("t")
    t.display()
