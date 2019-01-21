import time
from collections import namedtuple

import numpy as np

from lazynumpy.util import optimal_eval 

class _MasterMatricesManager:
	class __MasterMatricesManager:
		def __init__(self, lndarray_instance, arrays):
			self.pointer_to_matrices = {hash(time.time()): array.copy() for i, array in enumerate(arrays)}
			self.map_from_lndarrays_to_matrices = {hash(lndarray_instance): self.pointer_to_matrices.keys()}
			self.map_from_matrices_to_lndarrays = {array_p: hash(lndarray_instance) 
													for array_p in self.pointer_to_matrices.keys()}

		def append(self, lndarray_instance, arrays):
			self.map_from_lndarrays_to_matrices[hash(lndarray_instance)] = []
			for arr in arrays:
				arr_key = hash(time.time)
				self.pointer_to_matrices[hash(time.time)] = arr.copy()
				self.map_from_lndarrays_to_matrices[hash(lndarray_instance)].append(arr_key)
				self.map_from_matrices_to_lndarrays[arr_key] = hash(lndarray_instance)

		def __str__(self):
			return repr(self)

	instance = None
	def __init__(self, lndarray_instance, arrays):
		if not _MasterMatricesManager.instance:
			_MasterMatricesManager.instance = OnlyOne.__MasterMatricesManager(lndarray_instance, arrays)
		else:
			_MasterMatricesManager.instance.append(lndarray_instance, arrays)

	def __getattr__(self, lndarray_instance):
	    return _MasterMatricesManager.instance.map_from_lndarrays_to_matrices[hash(lndarray_instance)]

class _Evals():
	def __init__(self, val):
		if isinstance(val, list):
			self.vals = val
		else:
			self.vals = [val]

	def __mul__(self, other):
		# TODO: should we use extend instead so it overwrites the value in memory instead of a copy?
		return _Evals(self.vals + other.vals)

	def __call__(self):
		ordered_vals, _ = optimal_eval.Cost(self.vals, backtrack=True)
		return_val = optimal_eval.reduce_tree(ordered_vals, lambda x, y: np.matmul(x,y))
		return return_val


class lndarray(np.ndarray):
	def __new__(cls, obj, _hashname=None):
		obj = np.asarray(obj).view(cls)
		obj._hash = _hashname if _hashname else hash(time.time())
		obj._cls = cls
		obj._evals = _Evals(obj)
		return obj

	def __array_finalize__(self, obj):
		if obj is None:
			return
		self._hash = getattr(obj, '_hash', hash(time.time()))

	def ldot(self, other):
		""" If both a and b are 1-D arrays, it is inner product of vectors (without complex conjugation). 
			If both a and b are 2-D arrays, it is matrix multiplication, but using matmul or a @ b is preferred.
			If either a or b is 0-D (scalar), it is equivalent to multiply and using numpy.multiply(a, b) or a * b is preferred
			If a is an N-D array and b is a 1-D array, it is a sum product over the last axis of a and b.
			If a is an N-D array and b is an M-D array (where M>=2), it is a sum product over the last axis of a and the second-to-last axis of b:"""
		if len(self.shape) == 2 and len(other.shape) == 2 and isinstance(other, lndarray):
			new = lndarray(self)
			new._evals = self._evals * other._evals
			return new
		return self.dot(other) # otherwise use regular np dot

	def eval(self):
		val = self._evals()
		_hash = self._hash
		obj = np.asarray(val).view(self._cls)
		obj._hash = _hash
		return obj

	def __hash__(self):
		return self._hash