__author__ = 'shaughnfinnerty'


class Node:
    def __init__(self, id, is_factor_node):
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
