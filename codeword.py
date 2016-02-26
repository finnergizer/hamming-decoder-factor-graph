__author__ = 'shaughnfinnerty'

import numpy as np
import random


class Codeword:
    codeword_list = ["0000000",
                "0001011",
                "0010101",
                "0011110",
                "0100110",
                "0101101",
                "0110011",
                "0111000",
                "1000111",
                "1001100",
                "1010010",
                "1011001",
                "1100001",
                "1101010",
                "1110100",
                "1111111"]

    def __init__(self):
        self.codeword = Codeword.generate_random_codeword()
        return

    # This method will return an array representing the codeword with noise added to it
    def transmit(self, sd_noise):
        # TODO: Add Gaussian Noise
        def transform(x):
            if x == 1:
                return -1
            elif x == 0:
                return 1
        transmission = map(transform, self.codeword) + np.random.normal(0, sd_noise, len(self.codeword))
        self.transmission = transmission.tolist()
        return self.transmission

    @classmethod
    def generate_random_codeword(cls):
        return random.choice(Codeword.generate_codewords())
        # return list(random.choice(cls.codeword_list))

    @classmethod
    def generate_codewords(cls):
        eqs = np.matrix([[0, 0, 0, 1, 1, 1, 1],
                        [0, 1, 1, 0, 0, 1, 1],
                        [1, 0, 1, 0, 1, 0, 1]])
        result = []
        for i in range(0,128):
            num = np.matrix([int(n) for n in list(np.binary_repr(i, width=7))])
            prod = num * np.transpose(eqs)
            f = np.vectorize(lambda x: x % 2)
            prod = f(prod)

            if (not np.count_nonzero(prod)):
                result.append(np.array(num)[0].tolist())
        return result



# print Codeword.generate_random_codeword()
c = Codeword()
c.transmit(1)


