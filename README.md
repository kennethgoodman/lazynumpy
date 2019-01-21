
[![Build Status](https://travis-ci.org/kennethgoodman/lazy_numpy.svg?branch=master)](https://travis-ci.org/kennethgoodman/lazy_numpy)
[![codecov](https://codecov.io/gh/kennethgoodman/lazy_numpy/branch/master/graph/badge.svg)](https://codecov.io/gh/kennethgoodman/lazy_numpy)

# lazynumpy
a lazy evaluated wrapper around numpy

What is gained?

* Chained matrix multiplication will be minimized by keeping the values of the other arrays in memory and solving the associative problem that minimizes the number of computations.
  - only keeps one copy of each matrix [Memory optimization in progress]
* Allow partial matrix returns withou calculating the entire matrix [In Progress]
