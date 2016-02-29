__author__ = 'shaughnfinnerty'

import math
import codeword
import graph
import numpy as np

class Decoder:
    SUM_PROD = 0;
    MAX_PROD = 1;
    MAX_ITERATIONS = 20;

    def __init__(self, variance, mode=SUM_PROD):
        self.variance = variance;
        self.mode = mode
        self.noise = math.sqrt(variance)

    def initialize_decoder(self, transmission):
        g = graph.Graph()
        for id, node in g.nodes.iteritems():
            if not node.is_factor_node:
                for edge in node.outgoing_edges:
                    edge.messages.append([1, 1])
                node_num = int(list(id)[1])
                node.prior_prob = self.prior_probability(transmission[node_num - 1])
            else:
                for edge in node.outgoing_edges:
                    edge.messages.append(None)
        self.graph = g

    # Returns P(x=0|z) and P(x=1|z) for any x_i
    def prior_probability(self, z):
        p = lambda x: 1 - 1 / (1 + math.exp((1 - 2 * float(x)) * 4 * float(z) / math.pow(self.noise, 2)))
        # p = lambda x: math.exp(-1*(math.pow((float(z)-1+2*float(x)), 2)/(2*self.variance)))/(self.noise*math.sqrt(2*math.pi))
        return [p(0), p(1)]

    def compute(self, from_node, to_node, i):
        msg = self.graph.edges[from_node.id + "-->" + to_node.id].messages[i]
        if self.can_compute(from_node, to_node, i):
            if from_node.is_factor_node:
                incoming_msgs = []
                for edge in from_node.incoming_edges:
                    if not edge.from_node.id == to_node.id:
                        incoming_msgs.append(edge.messages[i])
                if self.mode == self.MAX_PROD:
                    msg = [self.sum_out_at(self.generate_product(incoming_msgs), 0),
                           self.sum_out_at(self.generate_product(incoming_msgs), 1)]
                elif self.mode == self.SUM_PROD:
                    msg = [self.max_out_at(self.generate_product(incoming_msgs), 0),
                           self.max_out_at(self.generate_product(incoming_msgs), 1)]

            else:
                msg = [1.0, 1.0]
                for edge in from_node.incoming_edges:
                    if not edge.from_node.id == to_node.id:
                        if not from_node.is_factor_node:
                            msg = [a * b for a, b in zip(msg, edge.messages[i])]
                        else:
                            # sum-prod
                            # msg = [msg[0]*(edge.messages[i][0] + edge.messages[i][1]), msg[1]*(edge.messages[i][0] + edge.messages[i][1])]
                            # max-prod
                            msg = [msg[0] * max(edge.messages[i]), msg[1] * max(edge.messages[i])]
                msg = [a * b for a, b in zip(msg, from_node.prior_prob)]

        self.graph.edges[from_node.id + "-->" + to_node.id].messages.append(msg)

    def sum_out_at(self, product, xa):
        sum = 0.0
        for config in range(0, 8):
            binary_config = [int(n) for n in list(np.binary_repr(config, width=3))]
            sum += product(xa, binary_config[0], binary_config[1], binary_config[2])
        return sum


    def max_out_at(self, product, xa):
        max = 0.0
        for config in range(0, 8):
            binary_config = [int(n) for n in list(np.binary_repr(config, width=3))]
            prod_at = product(xa, binary_config[0], binary_config[1], binary_config[2])
            if prod_at > max:
                max = prod_at
        return max

    def generate_product(self, incoming):
        def product(xa, xj, xk, xl):
            return incoming[0][xj] * incoming[1][xk] * incoming[2][xl] * self.generic_factor_function(xa, xj, xk, xl)

        return product

    def generic_factor_function(self, xa, xj, xk, xl):
        if ((xa + xj + xk + xl) % 2) == 0:
            return 1.0
        else:
            return 0.0

    def iterate(self, i):
        for id, node in self.graph.nodes.iteritems():
            for edge in node.outgoing_edges:
                self.compute(node, edge.to_node, i)


    def can_compute(self, from_node, to_node, i):
        for edge in from_node.incoming_edges:
            if edge.from_node.id != to_node.id and edge.messages[i] == None:
                return False
        return True

    # Compute the argmax for each xi to get xi', the most probable value of xi
    def compute_belief(self):
        results = []
        for i in range(1, 8):
            belief = [1.0, 1.0]
            node = self.graph.nodes["x" + str(i)]
            for edge in node.incoming_edges:
                belief = [a * b for a, b in zip(belief, edge.messages[-1])]
            belief = [a * b for a, b in zip(belief, node.prior_prob)]
            if belief[0] >= belief[1]:
                results.append(0)
            else:
                results.append(1)
        return results

    def decode(self, transmission):
        self.initialize_decoder(transmission)
        decoded = []
        for i in range(0, self.MAX_ITERATIONS):
            self.iterate(i)
            decoded = self.compute_belief()
            for cdwd in codeword.Codeword.generate_codewords():
                if cdwd == decoded:
                    return decoded
        print ("Did not find a codeword after " + str(self.MAX_ITERATIONS) + " iterations")
        return decoded

