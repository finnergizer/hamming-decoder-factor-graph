Hamming codes for 4 bit numbers 0-15 generated with 
http://www.ecs.umass.edu/ece/koren/FaultTolerantSystems/simulator/Hamming/HammingCodes.html


Resources:
http://www.iosrjournals.org/iosr-jce/papers/vol2-issue3/C0231224.pdf
http://kom.aau.dk/~tlj/mpa_lp_decoding_ldpc.pdf

Good one on Factor Graph from Parity Check Matrix H:
    - http://www.crm.sns.it/media/course/1524/Loeliger_A.pdf
    - IMPORTANT: The Delta function seen in this slide is the function that is 0 everywhere except at 0!!!!
    
http://www.telecom.tuc.gr/~alex/lectures/lecture5.pdf


Youtube:
    - https://www.youtube.com/watch?v=zhfX3h48GLA


http://pages.cs.wisc.edu/~jerryzhu/cs769/bp.pdf
    
http://www.psi.toronto.edu/~psi/pubs2/1999%20and%20before/134.pdf
    - This message-passing procedure is initiated at the leaf nodes in the factor-graph, i.e., 
    those nodes on which only a single edge is incident.


Notes:
    - Observed values should be represented in factor graph
   
   



http://cs-wwwarchiv.cs.unibas.ch/lehre/hs11/cs351/_Slides/Schoenborn_SumProduct.pdf
    - Initial messages from variables to factors becomed Dirac Delta???
    - Question for PROF: What are our initial messages given the fact that we have the Dirac Delta?
        - Should they just be the exact observed value sent as a message from the function to the variable?

Iterative Decoder
    - initialize messages = 1, then iterate until a valid codeword has been reached
        - from our notes, we are to only initialize all variable messages in cycles (outgoing from a variable node) to 1
        - https://en.wikipedia.org/wiki/Unit_function
    - stopping criterion: some time has passed (i.e. 10 iterations) OR a valid codeword has been reached
    -