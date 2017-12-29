# What is PPerfG
PPerfG is a utility program under PPerfTrack, and designed to compose diagrams
which visualizes the dataflow during a complete performance monitoring and
analysis process. The diagrams indicate connections between system components
(such like storage, network, memory), applications being monitored, and
monitoring and analysis components in the view of data generating, transferring
and modification. It is developed in Python 2.7, and uses Tkinter,
the Python’s standard GUI (Graphical User Interface) package, and Ttk which is
also built-in in Python to compose the interactive interface.

The ultimate goal of PPerfG is to provide the holistic dataflow diagram from
as high as campaign level, to job run level, to application level, and finally
to package level, and the interactive interface will allow users to inspect
in different levels to track the dataflow dynamically. Currently, at the early
developing stage, the majority tasks are focused on researching, design planning
and developing a prototype to validate the technical feasibility. So far,
the prototype can parse the source file and compose the diagram for job run
level successfully.

###Run PPerfG in command prompt
run **python main.py** and it will ask for a source filename.


# Some Technical Decisions
## Python and Tkinter
The main reason why choosing Python is because PPerfTrack is also developed in
Python, so using the same program language can reduce the number of dependencies
the PPerfTrack family requires.

Tkinter is Python's standard GUI (Graphical User Interface) package. It is
a thin object-oriented layer on top of Tck/Tk and is included in Python’s
standard installation. Although the functionalities Tkinter provides is limited,
and I have to implement a helper class on top of Tkinter to make tooltips on
canvas, it is still a good choice if we consider the purpose and requirement of
the project.

## Source File Design
PPerfG asks user for the source file which will be parsed to build up the
internal data structure for drawing the diagram eventually. The source file is
a single JSON file representing one diagram, and it will be treated as a
dictionary (one data type in Python) in the program. For detailed explanation
of the source file, please read “SourceFileDesignPlan.txt” under the project
directory.

## Data Structures: Node, Tree and List
The object Node is used to hold both dataset and task, dataset is drawn as
circle in the diagram and task is drawn as rectangle at the bottom of
the diagram. During the parsing process, nodes are created and appended to
a list which will be used later for building the tree and other manipulations.

The tree is used to represent the inner hierarchy of nodes. There are edges
between parents and children in the diagram with arrow indicating the direction
of the action. When building the tree, a node called root is added and its
children are all nodes which have no parent in the list. As a result, the tree
is a general tree and each node could have several parents and several children.

It is good to use a tree to represent the relations between nodes and efficient
to use some tree-related algorithm, but the list is still very important because
some operations cannot be done if we don’t have holistic analysis and
understanding of all nodes. For example, for each node we need to find out
the nodes on the same layer, to set initial coordinate, and to set the radius
depending on the overall distribution of dataset size. Traversing the list
instead of the tree is more efficient and doable for those needs.

## Overall Design of the Drawing Algorithm
The diagram is drawn on one canvas, so we need to calculate the coordinate of
each component before composing the final diagram. Layers and tasks are set as
the frame of the diagram, the positions of dataset circles are calculated by
analyzing its surrounding environment.

For each dataset circle, the y-axis coordinate is simply determined by the
layer it is on, the x-axis coordinate is a little complicated to calculated.
Firstly, we set initial x-axis coordinate the same as the average value of the
x-axis coordinates of its children, by doing this all nodes in the diagram have
an x-axis coordinate but the value might be duplicated or the circles might
overlap each other, therefore we need to adjust the x-axis value to eliminate
those errors. For each dataset circle, we check whether it has overlapping with
other circles on the same layer and adjust its x-axis value if it does, this
work is repeated until there is no overlapping.

Finally, the start and end coordinates of edges between nodes and the position
of the arrow are calculate using those nodes’ coordinates.

## Current State and Future Plan
So far, the prototype can parse the source file and compose the diagram for job
run level, and the unadorned diagram visualizes the information from the source
in a clear and readably format.

As mentioned above, the ultimate goal of PPerfG is to provide holistic dataflow
diagrams of different levels and an interactive interface for user to inspect
in different levels to track the dataflow dynamically. This prototype has
showed the possibility for making a such tool using existing technical tools
and resources. This is the very first attempt of PPerfG and there are still
a lot of room for improvement.

We need to find an algorithm to avoid the intersection of edges. In the current
version, edges could cross other edges and circles which makes the diagram
untidy and even confusing. Therefore, in future development we need to
design a new algorithm that makes the edges not go cross each other and keep
circles not overlap at the same time.

Another necessary improvement is about handling the duplications of datasets
in the diagram. It happens sometimes that a dataset is moved to a new position
and then is read or written to a task or dataset. So PPerfG should be smart
enough to know where to put the edge: should it start from the original dataset
or the duplicated one. One possible solution is to check the origin of
the event, which has not yet been done.

Due to the limit of time and the quite huge workload, a systemic testing
framework is not finished. There is some necessary error checking in most
functions, but there are no testing cases and testing scripts written at
current stage. Therefore, writing testing cases and testing scripts should be
considered in the following development.
