__author__ = 'shaughnfinnerty'

from decoder import Decoder
import codeword
import matplotlib.pyplot as plt
import math

class Simulator():

    def __init__(self, iterations, variance_levels):
        self.iterations = iterations
        self.variance_levels = variance_levels
        self.codewords = []
        self.decoded = []
        self.bit_error_probability = []

        return


    def simulate(self):
        for var in self.variance_levels:
            codewords = []
            decoded = []
            decoder = Decoder(var)
            for i in range(0, self.iterations):
                code = codeword.Codeword()
                codewords.append(code.codeword)
                decoded.append(decoder.decode(code.transmit(var)))
            self.codewords.append(codewords)
            self.decoded.append(decoded)

    def compute_error(self):
        for i in range(len(self.variance_levels)):
            errors = 0.0
            for j in range(len(self.codewords[i])):
                for k in range(len(self.codewords[i][j])):
                    # if self.codewords[i][j][k] != self.decoded[i][j][k]:
                    if 0 != self.decoded[i][j][k]:
                        errors += 1.0
            bit_error_prob = errors/(7*len(self.codewords[i]))
            self.bit_error_probability.append(bit_error_prob)

    def graph(self):
        plt.plot([math.log(x) for x in self.variance_levels], [math.log(y) for y in self.bit_error_probability])
        # plt.plot(self.variance_levels, self.bit_error_probability)
        plt.show()
        return



s = Simulator(100, [1, 0.5, 0.25, 0.125])
s.simulate()
s.compute_error()
s.graph()