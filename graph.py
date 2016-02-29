__author__ = 'shaughnfinnerty'


class Node:
    def __init__(self, id, is_factor_node):
        """
        Creates a node that keeps track of the
        :param id: The node id (e.g. x1) of this node
        :param is_factor_node: A boolean variable indicating that this node is a factor node. Used to indicate the
        requirement of different methods when computing messages.
        :return:
        """
        self.id = id
        self.is_factor_node = is_factor_node
        self.outgoing_edges = []
        self.incoming_edges = []

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id


class Edge:
    def __init__(self, from_node, to_node):
        """
        Initializes a directed edge with a reference to its originating and destination nodes.
        Messages are stored in an array so that they can be kept across iterations. NOTE:  even though this is
        directed, the graph is created in a way such that two directed edges are used to represent the one
        undirected edge of a factor graph
        :param from_node: the node from which the edge originates
        :param to_node: the node to which the edge points
        :return:
        """
        self.from_node = from_node
        self.to_node = to_node
        self.messages = []


    def __hash__(self):
        return hash(self.from_node + self.to_node)

    def __eq__(self, other):
        return (self.from_node, self.to_node) == (other.from_node, other.to_node)

    def __str__(self):
        return str(self.from_node) + "-->" + str(self.to_node)


class Graph:

    def __init__(self):
        """
        Creates a graph with node objects and edge objects that represent the factor graph seen in README that is used
        to represent the global function of this error corrected code.
        Stores each edge in a dictionary (hashmap) with keys of the form "x1-->f1" for quick access
        Stores each node in a dictionary (node) with keys of the form "x1" for quick access
        :return:
        """
        self.graph_string = {'x1': ["f1"],
                             "x2": ["f2"],
                             "x3": ["f1", "f2"],
                             "x4": ["f3"],
                             "x5": ["f1", "f3"],
                             "x6": ["f2", "f3"],
                             "x7": ["f1", "f2", "f3"],
                             "f1": ["x1", "x3", "x5", "x7"],
                             "f2": ["x2", "x3", "x6", "x7"],
                             "f3": ["x4", "x5", "x6", "x7"]}
        self.nodes = {}
        self.edges = {}
        for node, _ in self.graph_string.iteritems():
            n = None
            if node.startswith("x"):
                n = Node(node, False)
            elif node.startswith("f"):
                n = Node(node, True)
            self.nodes[n.id] = n
        for node, connections in self.graph_string.iteritems():
            n = self.nodes[node]
            for connection in connections:
                edge = None
                if self.nodes.get(connection):
                    edge = Edge(n, self.nodes[connection])
                n.outgoing_edges.append(edge)
                self.nodes[connection].incoming_edges.append(edge)
                self.edges[str(edge)] = edge

    def __str__(self):
        result = ""
        for id, node in self.nodes.iteritems():
            result += str(node) + " (" + str(node.is_factor_node) + ") :\n"
            for edge in node.outgoing_edges:
                result += str(edge) + "\n"
            result += "\n"
        return result
