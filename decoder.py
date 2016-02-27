__author__ = 'shaughnfinnerty'

import math
import codeword
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
        return [p(0), p(1)]

    def compute(self, from_node, to_node, i):
        msg = self.graph.edges[from_node.id + "-->" + to_node.id].messages[i]
        if self.can_compute(from_node, to_node, i):
            msg = [1.0, 1.0]
            for edge in from_node.incoming_edges:
                    if not edge.from_node.id == to_node.id:
                        msg = [a*b for a,b in zip(msg, edge.messages[i])]
            if from_node.is_factor_node:
                # 0.5 is the normalized factor calculation (from 4)
                # TODO: Use indicator factor function with Dirac delta to determine 0.5, 0.5 computationally
                msg = [a*b for a,b in zip(msg, [0.5,0.5])]
                # print msg
                # max-prod determination
                # if True:
                #     if msg[0] >= msg[1]:
                #         msg = [msg[0], msg[0]]
                #     else:
                #         msg = [msg[1], msg[1]]
            else:
                msg = [a*b for a,b in zip(msg, from_node.prior_prob)]
        self.graph.edges[from_node.id + "-->" + to_node.id].messages.append(msg)



    def iterate(self, i):
        for id, node in self.graph.nodes.iteritems():
            for edge in node.outgoing_edges:
                self.compute(node, edge.to_node, i)


    def can_compute(self, from_node, to_node, i):
        for edge in from_node.incoming_edges:
            if edge.from_node.id != to_node.id and edge.messages[i] == None:
                return False
        return True

    def compute_belief(self):
        results = []
        for i in range(1,8):
            belief = [1.0, 1.0]
            node = self.graph.nodes["x"+str(i)]
            for edge in node.incoming_edges:
                belief = [a*b for a,b in zip(belief, edge.messages[-1])]
            belief = [a*b for a,b in zip(belief, node.prior_prob)]
            if belief[0] >= belief[1]:
                results.append(0)
            else:
                results.append(1)
        return results

    def decode(self, transmission):
        self.initialize_decoder(transmission)
        decoded = []
        for i in range(0,20):
            self.iterate(i)
            decoded = self.compute_belief()
            for cdwd in codeword.Codeword.generate_codewords():
                if cdwd == decoded:
                    return decoded
        print ("Did not find a codeword after 20 iterations")
        return decoded






# d = Decoder(1)
# d.initialize_decoder([-0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5])
#
# # for i in range(0,10):
# #     d.iterate(i)
# #     print(d.compute_belief())
#
#
# for i in range(0,10):
#     code = codeword.Codeword()
#     print "codeword:" + str(code.codeword)
#     print "decoded:" + str(d.decode(code.transmit(1)))
#     print ""