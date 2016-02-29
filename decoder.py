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
        """
        Initializes a decoder for a channel with normal distribution centered at 0 and noise variance
        :param variance: variance of the normal distribution of channel noise
        :param mode: the mode 0, or 1 indicating decoding with sum-prod and max-prod, respectively
        :return:
        """
        self.variance = variance;
        self.mode = mode
        self.noise = math.sqrt(variance)
        self.graph = graph.Graph()

    def initialize_decoder(self, transmission):
        """
        Creates a new graph to begin the message passing, setting all messages from g_a to x_a for all x_a to the results
        computed from prior_probability.  Also sets the initial messages from variable nodes to factor nodes to [1,1] for
        domain values 0,1 respectively.
        :param transmission: The real-valued transmission with noise added to it. Necessary for computing prior probabilities
        :return:
        """
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

    #
    def prior_probability(self, z):
        """
        Computes P(x=0|z) and P(x=1|z) for any x_i and observed z_i
        :param z: The observed (i.e. received transmission bit)
        :return: an array representing the CDF (with mean -1 or 1 depending on x and variance that is known to the decoder)
        evaluated at z. (i.e. the likelihood that the hidden variable is 1 or 0 given its received value z)
        """
        p = lambda x: 1 - 1 / (1 + math.exp((1 - 2 * float(x)) * 4 * float(z) / math.pow(self.noise, 2)))
        return [p(0), p(1)]

    def compute(self, from_node, to_node, i):
        """
        Computes the message for from_node to to_node. If it is a variable node, compute the product the product of
        all incoming messages, otherwise, compute the factor node message by summing/maximizing the product of the local
        function with all incoming messages (except the one from the to_node) over all neighbouring variables (except
        the variable represented by to_node)
        :param from_node: the node from which the msg is being sent/originating
        :param to_node: the node to which the msg is being sent
        :param i: The discrete time interval that we are on in the message passing schedule (so that we can retrieve the
        most up-to-date messages during computation)
        :return:
        """
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
                # initialize to 1 so that following multiplication doesn't result in 0
                msg = [1.0, 1.0]
                for edge in from_node.incoming_edges:
                    if not edge.from_node.id == to_node.id:
                        msg = [a * b for a, b in zip(msg, edge.messages[i])]

                # Multiply by the last incoming message (i.e. from factor g_a) which does not change
                msg = [a * b for a, b in zip(msg, from_node.prior_prob)]

        self.graph.edges[from_node.id + "-->" + to_node.id].messages.append(msg)

    def generate_product(self, incoming):
        """
        Returns the product of all incoming messages with the local factor function at a factor node
        :param incoming: An array with each element representing function/message from a neighbour (that is not the
         destination)
        :return:
        """

        def product(xa, xj, xk, xl):
            return incoming[0][xj] * incoming[1][xk] * incoming[2][xl] * self.generic_factor_function(xa, xj, xk, xl)

        return product

    def generic_factor_function(self, xa, xj, xk, xl):
        """
        Returns the value of a factor given its four parameter bits.
        Since all factor functions are essentially the same (but with different variables),
        this generic function is used to represent the local function at each factor node.
        :param xa: first bit in factor
        :param xj: second bit in factor
        :param xk: third bit in factor
        :param xl: fourth bit in factor
        :return:
        """
        if ((xa + xj + xk + xl) % 2) == 0:
            return 1.0
        else:
            return 0.0

    def sum_out_at(self, product, xa):
        """
        Computes the value of the function at xa resulting from summing over all variables except Xa
        :param product: A function with four parameters. We can keep this at four since we are not solving the general case
         and simply a specific code.
        :param xa: The value to evaluate the resulting function from summing over all variables except Xa
        :return: the result of evaluating with Xa=xa the function of the product summed over all variables except Xa
        """
        sum = 0.0
        # We use a binary representation of 0-7 inclusive to represent all different configurations that the discrete
        # variables can have and sum over all these configurations
        for config in range(0, 8):
            binary_config = [int(n) for n in list(np.binary_repr(config, width=3))]
            sum += product(xa, binary_config[0], binary_config[1], binary_config[2])
        return sum


    def max_out_at(self, product, xa):
        """
        Computes the value of the function at xa resulting from maximize over all variables except Xa
        :param product: A function with four parameters. We can keep this at four since we are not solving the general case
         and simply a specific code.
        :param xa: The value to evaluate the resulting function from maximizing over all variables except Xa
        :return: the result of evaluating with Xa=xa the function of the product maximized over all variables except Xa
        """
        max = 0.0
        # We use a binary representation of 0-7 inclusive to represent all different configurations that the discrete
        # variables can have
        for config in range(0, 8):
            binary_config = [int(n) for n in list(np.binary_repr(config, width=3))]
            prod_at = product(xa, binary_config[0], binary_config[1], binary_config[2])
            if prod_at > max:
                max = prod_at
        return max


    def iterate(self, i):
        """
        Compute messages in another iteration of message passing
        :param i: The current iteration, used to identify the most recent message
        :return:
        """
        for id, node in self.graph.nodes.iteritems():
            for edge in node.outgoing_edges:
                self.compute(node, edge.to_node, i)

    def can_compute(self, from_node, to_node, i):
        """
        Checks whether there are incoming messages from every neighbour node except to_node
        :param from_node: the node from which the msg is wanting to be sent/originate
        :param to_node: the node to which the msg is wanting to be sent
        :param i: The current iteration of messaged, used to identify the most recent message
        :return: True if the from_node has incoming messages from all neighbour nodes except to_node, False otherwise
        """
        for edge in from_node.incoming_edges:
            if edge.from_node.id != to_node.id and edge.messages[i] == None:
                return False
        return True


    def compute_belief(self):
        """
        Compute the argmax for each xi to get xi'. Computes the product of all incoming messages at each variable node,
        and returns the value of xi that makes this product a maximum
        :return: A 7 bit codeword of bits that maximize the global function represented by the factor graph
        """
        results = []
        for i in range(1, 8):
            belief = [1.0, 1.0]
            # Get the current node i
            node = self.graph.nodes["x" + str(i)]
            for edge in node.incoming_edges:
                belief = [a * b for a, b in zip(belief, edge.messages[-1])]
            # multiply the product of all incoming messages by the incoming message from the factor g_i
            belief = [a * b for a, b in zip(belief, node.prior_prob)]
            if belief[0] >= belief[1]:
                # xi=0 maximizes
                results.append(0)
            else:
                # xi=1 maximizes
                results.append(1)
        return results

    def decode(self, transmission):
        """
        Intialize the graph and begin decoding using the algorithm specified by mode in the object.
        :param transmission: The real-valued 7 bit transmission received with channel noise
        :return: The decoded message that is one of the 16-bit codewords or the final 7-bit codeword decoded after
        MAX_ITERATIONS has been reached.
        """
        self.initialize_decoder(transmission)
        decoded = []
        # Only iterate up until MAX_ITERATIONS static int
        for i in range(0, self.MAX_ITERATIONS):
            self.iterate(i)
            decoded = self.compute_belief()
            for cdwd in codeword.Codeword.generate_codewords():
                # We have decoded a codeword that exists in the 16 codewords for this error code
                if cdwd == decoded:
                    return decoded
        print ("Did not find a codeword after " + str(self.MAX_ITERATIONS) + " iterations")
        return decoded

