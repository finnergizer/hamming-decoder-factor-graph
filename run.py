__author__ = 'shaughnfinnerty'

from simulator import Simulator
from decoder import Decoder
import sys

def run():
    if (sys.argv[1] == "-advanced"):
        s = Simulator(2000, [1, 0.5, 0.25, 0.125])
        s.simulate(Decoder.SUM_PROD)
        s.compute_error()
        s.save_results()
        s.plot('ro-')
        s.save_graph()

        s = Simulator(2000, [1, 0.5, 0.25, 0.125])
        s.simulate(Decoder.MAX_PROD)
        s.compute_error()
        s.save_results()
        s.plot('g^--')
        s.save_graph()

        s = Simulator(1000, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        s.simulate(Decoder.SUM_PROD)
        s.compute_error()
        s.save_results()
        s.plot('ro--')
        s.save_graph()

        s = Simulator(1000, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        s.simulate(Decoder.MAX_PROD)
        s.compute_error()
        s.save_results()
        s.plot('g^--')
        s.save_graph()
    else:
        print sys.argv
        print "Running default simulation at variance levels %(var)s with %(num)s codewords" % \
              {"var": [1, 0.5, 0.25, 0.125],
               "num": sys.argv[1]}
        s = Simulator(int(sys.argv[1]), [1, 0.5, 0.25, 0.125])
        s.default_run()

run()