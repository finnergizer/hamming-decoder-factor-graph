__author__ = 'shaughnfinnerty'

import numpy as np
import random

class Message:
    codeword = ["0000000",
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
        return

    # This method will return an array representing the codeword with noise added to it
    def transmit(self):
        # TODO: Add Gaussian Noise
        return

    @classmethod
    def generate_random_codeword(cls):
        return list(random.choice(cls.codeword))


print Message.generate_random_codeword()



