__author__ = 'shaughnfinnerty'

from decoder import Decoder
import codeword
import matplotlib.pyplot as plt
import math
import time
import csv
import os

class Simulator():
    USE_0_COMPARISON = False;

    def __init__(self, iterations, variance_levels):
        self.iterations = iterations
        self.variance_levels = variance_levels
        self.codewords = []
        self.decoded = []
        self.transmissions = []
        self.bit_error_probability = []
        self.save_time = ""

    def simulate(self, mode=Decoder.SUM_PROD):
        """

        :param mode: The algorithm (sum-prod vs max-prod) to use in the decoder simulations
        :return:
        """
        self.mode = mode
        self.codewords = []
        self.decoded = []
        for var in self.variance_levels:
            codewords = []
            decoded = []
            transmissions = []
            decoder = Decoder(var, self.mode)
            for i in range(0, self.iterations):
                code = codeword.Codeword()
                codewords.append(code.codeword)
                decoded.append(decoder.decode(code.transmit(var)))
                transmissions.append(code.transmission)
            self.codewords.append(codewords)
            self.decoded.append(decoded)
            self.transmissions.append(transmissions)

    def compute_error(self):
        """
        Computes the number of incorrectly coded bits over the total number of bits transmitted and appends this result
        to the array of bit_error_probabilities so that other variances can continue to be simulated.
        :return:
        """
        self.bit_error_probability = []
        for i in range(len(self.variance_levels)):
            # Start with 1.0 so that if bit error probability is 0, we do not have a domain error when eventually
            # converting to logarithmic scale if there are no errors at a given variance (i.e. lower variances)
            errors = 1.0
            for j in range(len(self.codewords[i])):
                for k in range(len(self.codewords[i][j])):
                    # Project says we can assume that decoder has no knowledge of original codeword, but we provide
                    # the option of comparing to the originak codeword
                    if self.USE_0_COMPARISON:
                        if 0 != self.decoded[i][j][k]:
                            errors += 1.0
                    else:
                        if self.codewords[i][j][k] != self.decoded[i][j][k]:
                            errors += 1.0

            bit_error_prob = errors / (7 * len(self.codewords[i]))
            self.bit_error_probability.append(bit_error_prob)


    def save_results(self):
        """
        Saves the bit_error_probability and corresponding variance in a csv file
        Saves the codewords, their transmissions, and their resulting decoding in files separted by channel noise variance
        :return:
        """
        self.save_time = epoch_time = str(int(time.time()))
        if not os.path.exists("./stats/advanced-run"):
            os.makedirs("./stats/advanced-run")
        m = "sum-prod" if self.mode == Decoder.SUM_PROD else "max-prod"
        with open("stats/advanced-run/%(time)s-%(mode)s-%(num_codewords)s-codewords-variance-bit_error_probability.csv" % {
        "time": epoch_time,
        "mode": m,
        "num_codewords": self.iterations}, 'wb') as result_csv:
            writer = csv.writer(result_csv)
            writer.writerow(["variance", "bit_error_probability"])
            for v, error in zip(self.variance_levels, self.bit_error_probability):
                writer.writerow([v, error])
        for i, v in enumerate(self.variance_levels):
            with open("stats/advanced-run/%(time)s-%(mode)s-%(num_codewords)s-codewords-variance-%(var)s-codewords-decoded.csv" % {
            "time": epoch_time,
            "mode": m,
            "num_codewords": str(self.iterations),
            "var": str(v)}, 'wb') as result_csv:
                writer = csv.writer(result_csv)
                writer.writerow(["codeword", "decoded", "transmission"])
                for codeword, transmission, decoded in zip(self.codewords[i], self.transmissions[i], self.decoded[i]):
                    writer.writerow([''.join(str(elem) for elem in codeword),
                                     ''.join(str(elem) for elem in decoded),
                                     ' '.join(str(elem) for elem in transmission)])

    def plot(self, style):
        """
        Clears the plot, and Plots current levels of variance vs. their bit_error_probability on a figure
        :param style: The style of the points and lines to plot the current dataset of variance and bit error probability
        :return:
        """
        plt.clf()
        plt.plot([math.log10(x) for x in self.variance_levels], [math.log10(y) for y in self.bit_error_probability],
                 style)
        # plt.plot(self.variance_levels, self.bit_error_probability)
        return

    def save_graph(self):
        """
        Saves the graph as a png. Used to save individuals algorithm simulations and plots.
        :return:
        """
        if not os.path.exists("./graphs/advanced-run"):
            os.makedirs("./graphs/advanced-run")

        m = "Sum-Prod" if self.mode == Decoder.SUM_PROD else "Max-Prod"
        plt.title("Hamming Decoder Factor Graph Simulation Results\n" +
                  r"$\log_{10}(\sigma^2)$ vs. $\log_{10}(P_e)$" + " for %(mode)s Algorithms\n" % {"mode": m} +
                  "Sample Size n = %(codewords)s Codewords \n Variance Levels = %(levels)s"
                  % {"codewords": str(self.iterations), "levels": str(self.variance_levels)})
        plt.xlabel("$\log_{10}(\sigma^2)$")
        plt.ylabel(r"$\log_{10}(P_e)$")
        plt.savefig("graphs/advanced-run/%(time)s-%(mode)s-%(num_codewords)s-codewords-variance-bit_error_probability.png" %
                    {"time": self.save_time,
                     "mode": m,
                     "num_codewords": self.iterations}, bbox_inches="tight")

    def default_run(self):
        """
        Plots the results, saves the figure, and finally displays it from simulating codewords with Sum-prod and Max-prod
        algorithms across variance levels. This combines the results in one plot.
        :return:
        """
        if not os.path.exists("./graphs"):
            os.makedirs("./graphs")
        self.save_time = str(int(time.time()))
        self.simulate(Decoder.SUM_PROD)
        self.compute_error()
        plt.plot([math.log10(x) for x in self.variance_levels], [math.log10(y) for y in self.bit_error_probability],
                 "ro-", label="Sum-Prod")
        self.simulate(Decoder.MAX_PROD)
        self.compute_error()
        plt.plot([math.log10(x) for x in self.variance_levels], [math.log10(y) for y in self.bit_error_probability],
                 "g^--", label="Max-Prod")
        plt.legend(loc=2)
        plt.title("Hamming Decoder Factor Graph Simulation Results\n" +
                  r"$\log_{10}(\sigma^2)$ vs. $\log_{10}(P_e)$" + " for Max-Prod & Sum-Prod Algorithms\n" +
                  "Sample Size n = %(codewords)s Codewords \n Variance Levels = %(levels)s"
                  % {"codewords": str(self.iterations), "levels": str(self.variance_levels)})
        plt.xlabel("$\log_{10}(\sigma^2)$")
        plt.ylabel(r"$\log_{10}(P_e)$")
        plt.savefig("graphs/%(time)s-max-prod-sum-prod-%(num_codewords)s-codewords-variance-bit_error_probability.png" %
                    {"time": self.save_time,
                     "num_codewords": str(self.iterations)}, bbox_inches="tight")
        plt.show()
