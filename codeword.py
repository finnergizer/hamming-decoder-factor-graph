__author__ = 'shaughnfinnerty'

import numpy as np
import random
import math


class Codeword:
    # codeword_list = generate_codewords()

    def __init__(self):
        """
        Initializes a codeword object with a randomly generated codeword.
        :return:
        """
        self.codeword = Codeword.generate_random_codeword()
        self.transmission = ""

    def transmit(self, variance):
        """
        This method will return an array representing the codeword with noise added to it
        :param variance: The variance of the Gaussian distribution to be sampled when randomly adding noise
        :return: An array representing the codeword with random samples of Gaussian noise added to each bit
        """

        def transform(x):
            if x == 1:
                return -1
            elif x == 0:
                return 1

        transmission = map(transform, self.codeword) + np.random.normal(0, math.sqrt(variance), len(self.codeword))
        self.transmission = transmission.tolist()
        return self.transmission

    @classmethod
    def generate_random_codeword(cls):
        """
        Using the idea that each codeword is equally likely to be transmitted, we randomly select one with this method.
        :return: A random selection from the possible codewords for the project's error code
        """
        return random.choice(Codeword.generate_codewords())
        # return list(random.choice(cls.codeword_list))

    @classmethod
    def generate_codewords(cls):
        """
        Generates a list of codewords that are valid given the projects parity check matrix H.
        :return: The list of possible codewords valid for the parity check matrix
        """
        pchk_matrix = np.matrix([[0, 0, 0, 1, 1, 1, 1],
                                 [0, 1, 1, 0, 0, 1, 1],
                                 [1, 0, 1, 0, 1, 0, 1]])
        result = []
        for i in range(0, 128):
            num = np.matrix([int(n) for n in list(np.binary_repr(i, width=7))])
            prod = num * np.transpose(pchk_matrix)
            f = np.vectorize(lambda x: x % 2)
            prod = f(prod)
            if not np.count_nonzero(prod):
                result.append(np.array(num)[0].tolist())
        return result
