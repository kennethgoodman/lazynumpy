""" larray class with lndarray """

import warnings

import numpy as np

from lazynumpy.internals.evals import _Evals


# pylint: disable=protected-access,invalid-name,fixme
class lndarray(np.ndarray):
    """ class for lazy n-dimensionary array """

    def __new__(cls, obj, _hashname=None):
        self = np.asarray(obj).view(cls)
        if len(self.shape) == 1:  # TODO: not the right way to do it, should be able to handle
            return lndarray(self.reshape(self.shape[0], -1))
        if len(self.shape) > 2:
            warnings.warn("Should not be using lndarray with more "
                          "than 2-D arrays (0, 1 and 2 will work fine)",
                          stacklevel=3)
        self._cls = cls
        self._evals = _Evals(self)
        return self


    # pylint: disable=attribute-defined-outside-init
    def ldot(self, other):
        """ [TODO] - If both a and b are 1-D arrays, it is inner
                            product of vectors (without complex conjugation).
			[DONE] - If both a and b are 2-D arrays, it is matrix multiplication,
			                but using matmul or a @ b is preferred.
			[DONE] - If either a or b is 0-D (scalar), it is equivalent to multiply and
			                using numpy.multiply(a, b) or a * b is preferred
			[TODO] - If a is an N-D array and b is a 1-D array, it is a
			                sum product over the last axis of a and b.
			[TODO] - If a is an N-D array and b is an M-D array (where M>=2),
			                it is a sum product over the last axis of a
			                and the second-to-last axis of b
		"""
        if (len(self.shape) == 2 and len(other.shape) == 2) or \
                not other.shape or \
                not self.shape:  # if both 2d array, or one is 0d array
            new = lndarray(self.copy())
            new._evals = self._evals * other._evals
            return new
        warnings.warn("Should not be using lndarray with ldot if "
                      "both are not lndarray with dimensions <= 2",
                      stacklevel=3)
        return lndarray(np.dot(self, other))  # otherwise use regular np dot
    # pylint: enable=attribute-defined-outside-init

    def eval(self):
        """

        :return: evaluates saved matrix operations
        """
        val = self._evals()
        return lndarray(val)
# pylint: enable=protected-access,invalid-name,fixme
