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
    parent = []
    children = []
    placed_layer = -1
    name = ""
    # if it is a dataset
    size = 0
    data_type = ""
    # if it is a task
    runtime = 0
    collectionTool = ""

    def __init__(self, name):
        """the very basic constructor of the class

        Since the node might be either a dataset or a task, so we leave
        setting values to other functions. But 'name' is a must-have attribute
        for both, so we set the name in this basic constructor.

        Arg:
            name (string): the name of the node
        """
        self.name = name

    def display(self):
        """display the content of the current node in a clear format
        """
        print "- - - - - - - - "
        print "name: ", self.name
        print "size: ", self.size
        print "data type: ", self.data_type
        print "placed_layer: ", self.placed_layer
        print "runtime: ", self.runtime
        print "collectionTool: ", self.collectionTool
        print "parent: "
        if self.parent != 0:
            for item in self.parent:
                print " ", item.name
        print "children: "
        if self.children != 0:
            for item in self.children:
                print " ", item.name
        return

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
        return

    def set_child(self, child_node):
        """set the child of the current node

        Arg:
           child_node (Node): the node representing child
        """
        if child_node != 0:
            self.children.append(child_node)
        return

    def set_placed_layer(self, placed_layer):
        """set the placed_layer of the current node

        Arg:
            placed_layer (int): the layer the current node placed in the tree
        """
        if placed_layer != "":
            self.placed_layer = placed_layer
        return


if __name__ == '__main__':
    p = Node("p", 10, "binary file", None, None)
    c1 = Node("c1", 5, "child file", None, None)
    c2 = Node("c2", 8, "child file", None, None)
    t = Node("t", 100, "tset file", p, [c1, c2])
    t.display()
