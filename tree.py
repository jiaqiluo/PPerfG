import globalVariables as gv


class Node:
    """This class contains data members and functions of a Node

    Attributes:
        name (string): the name of the node
        parent (list of Node): the list of parents of the current node
        children (list of Node): the list of children of the current node
        same_layer_nodes (list of Node): the list of node with the same layer
        direction (list of int): the list of directions between this node and
                                 nodes in children list
        layer_name (string): the name of the layer this node placed
        layer_idx (int): the index of the the layer this node placed
        coordinate ([x,y]): the coordinate of this node in the diagram
        size (int): the size of the dataset, initial value is 0
        radius (float): the radius of the circle if the node is a dataset
        data_type (string): the data type of the dataset
        is_copy (int): whether this node is duplicated in the diagram
        runtime (int): how long the task runs, intial value is 0
        collectionTool (string): the name of the tool used to collect the data
    """
    radius_list = [] # radiuses apprearing in all node

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
        self.same_layer_nodes = []
        self.direction = []
        self.layer_name = ""
        self.layer_idx = -1
        self.coordinate = [0, 0]
        # if it is a dataset
        self.size = 0
        self.radius = 0
        self.data_type = ""
        self.is_copy = 0
        # if it is a task
        self.runtime = 0
        self.collectionTool = ""

    def copy_dataset_info(self, source):
        """
        """
        self.size = source.size
        self.radius = source.radius
        self.data_type = source.data_type
        self.is_copy = 1

    def traverse_display(self, n):
        """traverse the tree to display names,
        using indends to show parent-children relation

        Args:
            n (int): the degree of indend
        """
        for i in self.children:
            i.traverse_display(n + 1)
        if len(self.children) == 0:
            print "   " * n, "name:", self.name, "(leaf, coord:", self.get_coord(
            ), ")"
        else:
            print "   " * n, "name: ", self.name
        return

    def set_temp_coord(self):
        """set temp coordinate for each node, which is prepared for adjust_x

        Return:
            x_list (list): a list of x-coordinate of children
        """
        x_list = []
        for item in self.children:
            temp = item.set_temp_coord()
            for t in temp:
                x_list.append(t)
        t = self.coordinate[0]
        if t != 0:
            x_list.append(t)
        x_list.sort()
        if self.radius > 0:
            if len(x_list) != 0:
                avg = sum(x_list) / len(x_list)
            else:
                avg = gv.window_width/2
            if self.coordinate == [0, 0]:
                self.coordinate = [
                    avg, (self.layer_idx - 0.5) * gv.layer_height + 10
                ]
        # print "  " * ident, self.name, x_list, "| coord:",self.coordinate, "r=", self.radius
        return x_list

    def adjust_x_helper(self):
        """adjust the x-coordinate of each node to forbid overlapping of nodes
        """
        used_x = []
        final_x = self.coordinate[0]
        left_boundary = gv.layer_name_width + gv.radius_max
        right_boundary = gv.layer_width - gv.radius_max
        # print "adjust_x - ", self.name
        for item in self.same_layer_nodes:
            x = item.coordinate[0]
            # print "from ", item.name, "r= ", item.radius, "x= ", item.coordinate[0]
            if x not in used_x:
                used_x.append(x)
        count = len(used_x)
        while count > 0:
            for t in used_x:
                if abs(t - final_x) >= gv.radius_max * 2:
                    count -= 1
                else:
                    final_x += gv.radius_max * 2
                    count += 1
        self.coordinate[0] = final_x
        return

    def adjust_x(self):
        """recursivly traverse the tree to adjust x-coordinate
        """
        for node in self.children:
            node.adjust_x()
        if self.size != 0:
            self.adjust_x_helper()
        else:
            return

    def get_edge(self):
        """return the list of edges of a node

        Return:
            edge_list: the format of element of the list:
                            [[start coordinate], [end coordinate], direction]
        """
        edge_list = []
        length = len(self.children)
        if length != 0:
            for i in range(length):
                edge_list.append([[
                    self.coordinate[0], self.coordinate[1] + self.radius
                ], [
                    self.children[i].coordinate[0],
                    self.children[i].coordinate[1] - self.children[i].radius
                ], self.direction[i]])
        return edge_list

    def display(self):
        """display the content of the current node in a clear format
        """
        print "- - - - - - - - "
        print "name: ", self.name
        print "size: ", self.size
        print "data type: ", self.data_type
        print "layer_name: ", self.layer_name
        print "layer_idx: ", self.layer_idx
        print "coordinate: ", self.coordinate
        print "radius: ", self.radius
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
        print "same layer nodes: "
        for item in self.same_layer_nodes:
            print item.get_name()
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
        """return the node's dataset size

        Return:
            size (float): the dataset size
        """
        return self.size

    def set_type(self, data_type):
        """set the datatype of the current node if it is a dataset

        Arg:
            data_type (string): the datatype of the dataset
        """
        if data_type != "":
            self.data_type = data_type
        return

    def get_type(self):
        """return the node's data_type

        Return:
            data_type (string): the data_type
        """
        return self.data_type

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
        """return the list of the node's parent if it is not empty

        Return:
            parent (list): the node's parent list
        """
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
            idx (int): the index of the placed layer
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
                        1 - from the current node to child
                            OR move from the current node to child
                        2 - from child to the current node
                        3 - two-drection arrow
        """
        if mode in [0, 1, 2, 3]:
            self.direction.append(mode)
        else:
            print("invalid mode value")
        return

    def set_radius(self, radius):
        """set the node's radius
        """
        if radius != 0:
            self.radius = radius
        return

    def get_radius(self):
        """return the node's radius

        Return:
            radius (float): the node's radius
        """
        return self.radius

    def set_coord(self, coord):
        """set the node's coordinate

        Arg:
            coord ([x, y]): a x,y pair
        """
        self.coordinate = coord
        return

    def get_coord(self):
        """return the node's coordinate

        Return:
            coordinate ([x,y]): the node's coordinate
        """
        return self.coordinate

    def set_same_layer_node(self, node):
        """save the nodes at the same layer to a list

        Arg:
            node (Node): a node
        """
        if node not in self.same_layer_nodes and node != self:
            self.same_layer_nodes.append(node)
        return

    def set_name(self, name):
        """set the node's name

        Arg:
            name (string): a new name
        """
        if name != "":
            self.name = name
        else:
            print "invalud name"
        return

    def get_name(self):
        """return the node's name

        Return:
            name (string): the node's name
        """
        return self.name


if __name__ == '__main__':
    t = Node("t")
    t.display()
