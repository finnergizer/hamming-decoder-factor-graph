

<script type="text/javascript" src="https://www.draw.io/js/embed-static.min.js"></script>


## Introduction

In this project we use two algorithms, sum-product and max-product on factor graphs with cycles to

![Factor Graph](images/factor-graph-hamming-code.svg)

Since the factor nodes $g_1..g_7$ have only degree one after being evaluated using function `Decoder.compute_prior_prob(x, z)` which computes the CDF of the normal distribution with the variance of the channel (we assume that channel noise is known to the decoder) and are purely a univariate function of x1..x7 respectively, then their message $u_{g_a-->x_a}(x_a)$ will never change and so we include this message in the variable nodes implicitly and use it when computing messages from variable nodes throughout the iterations of the algorithm.

$$

a^2

$$


a
