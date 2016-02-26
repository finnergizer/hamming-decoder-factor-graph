from unittest import TestCase

__author__ = 'shaughnfinnerty'

from decoder import Decoder

class TestDecoder(TestCase):
    def test_prior_probability(self):
        d = Decoder(1)
        print d.prior_probability(-1)
        print d.prior_probability(3.0)
        print d.prior_probability(0)