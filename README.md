
[![Build Status](https://travis-ci.org/kennethgoodman/lazy_numpy.svg?branch=master)](https://travis-ci.org/kennethgoodman/lazy_numpy)

# lazy_numpy
a lazy evaluated wrapper around numpy

What is gained?

* Chained matrix multiplication will be minimized by keeping the values of the other arrays in memory and solving the associative problem that minimizes the number of computations.
  - only keeps one copy of each matrix
* Allow partial matrix returns withou calculating the entire matrix
