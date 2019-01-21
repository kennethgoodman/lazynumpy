
[![Build Status](https://travis-ci.org/kennethgoodman/lazy_numpy.svg?branch=master)](https://travis-ci.org/kennethgoodman/lazy_numpy)
[![codecov](https://codecov.io/gh/kennethgoodman/lazy_numpy/branch/master/graph/badge.svg)](https://codecov.io/gh/kennethgoodman/lazy_numpy)

# lazynumpy
a lazy evaluated wrapper around numpy

What is gained?

* Chained matrix multiplication will be minimized by keeping the values of the other arrays in memory and solving the associative problem that minimizes the number of computations.
  - only keeps one copy of each matrix [Memory optimization in progress]
* Allow partial matrix returns withou calculating the entire matrix [In Progress]


If you have three matrices with dimensions as below there are two ways to do the matrix multiplication to find the answer:

<a href="https://www.codecogs.com/eqnedit.php?latex=A_{1000\&space;*\1}&space;*&space;B_{1\&space;*\1000}&space;*&space;C_{1000\&space;*\1000}&space;=&space;D_{1000\&space;*\1000}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?A_{1000\&space;*\1}&space;*&space;B_{1\&space;*\1000}&space;*&space;C_{1000\&space;*\1000}&space;=&space;D_{1000\&space;*\1000}" title="A_{1000\ *\1} * B_{1\ *\1000} * C_{1000\ *\1000} = D_{1000\ *\1000}" /></a>

Either:

<a href="https://www.codecogs.com/eqnedit.php?latex=[1]\&space;\&space;(A_{1000\&space;*\1}&space;*&space;B_{1\&space;*\1000})&space;*&space;C_{1000\&space;*\1000}&space;=&space;D_{1000\&space;*\1000}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[1]\&space;\&space;(A_{1000\&space;*\1}&space;*&space;B_{1\&space;*\1000})&space;*&space;C_{1000\&space;*\1000}&space;=&space;D_{1000\&space;*\1000}" title="[1]\ \ (A_{1000\ *\1} * B_{1\ *\1000}) * C_{1000\ *\1000} = D_{1000\ *\1000}" /></a>

or

<a href="https://www.codecogs.com/eqnedit.php?latex=[2]\&space;\&space;A_{1000\&space;*\1}&space;*&space;(B_{1\&space;*\1000}&space;*&space;C_{1000\&space;*\1000})&space;=&space;D_{100\10001000}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[2]\&space;\&space;A_{1000\&space;*\1}&space;*&space;(B_{1\&space;*\1000}&space;*&space;C_{1000\&space;*\1000})&space;=&space;D_{100\10001000}" title="[2]\ \ A_{1000\ *\1} * (B_{1\ *\1000} * C_{1000\ *\1000}) = D_{100\10001000}" /></a>

[1] will take `1000 * 1 * 1000` operations to calculate `A * B` plus `1000 * 1000 * 1000` operations to calculate `(A * B) * C`. The total sum to calculate `A * B * C` is equal to `1000^3 + 1000^2`.

[2] will take `1 * 1000 * 1000` operations to calculate `B * C` plus `1000 * 1 * 1000` operations to calculate `A * (B * C)`. The total sum to calculate `A * B * C` is equal to `1000^2 + 1000^2` which means the optimal multiplication order will be ~500 faster.

If you run [the simple example](https://github.com/kennethgoodman/lazynumpy/blob/master/examples/simple_faster_calculation.py) you should see a significant speed up. On my computer there is a 50x speedup with only three matrix calculations.
