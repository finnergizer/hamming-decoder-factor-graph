__author__ = 'shaughnfinnerty'

import math
import graph

class Decoder:

    def __init__(self, variance):
        self.variance = variance;
        self.noise = math.sqrt(variance)

    def initialize_decoder(self, transmission):
        g = graph.Graph()
        for id, node in g.nodes.iteritems():
            if not node.is_factor_node:
                for edge in node.outgoing_edges:
                    edge.messages.append([1, 1])
                node_num = int(list(id)[1])
                node.prior_prob = self.prior_probability(transmission[node_num-1])
            else:
                for edge in node.outgoing_edges:
                    edge.messages.append(None)
        self.graph = g

    def initialize_messages(self):
        return

    # Returns P(x=0|z) and P(x=1|z) for any x_i
    def prior_probability(self, z):
        p = lambda x: 1-1/(1 + math.exp((1-2*float(x))*4*float(z)/math.pow(self.noise, 2)))
        # p = lambda x: math.exp(-1*(math.pow((float(z)-1+2*float(x)), 2)/(2*self.variance)))/(self.noise*math.sqrt(2*math.pi))
        return (p(0), p(1))

    def compute(self):
        return None

    def iterate(self, i):
        return None

    def can_compute(self, node, i):
        for edge in node.edges:
                return
        return True


d = Decoder(1)
d.initialize_decoder([-1,0,0,0,0,0,0])

