from lazynumpy.larray import lndarray
import numpy as np


def test_two_matrices():
	A = lndarray(np.random.random((3, 1)))
	B = lndarray(np.random.random((1, 3)))
	C_expected = A.dot(B)
	C_actual = A.ldot(B) # currently lazy
	C_actual = C_actual.eval() # get value
	assert C_actual.shape == C_expected.shape
	assert np.array_equal(C_actual, C_expected)


def test_three_matrices():
	A = lndarray(np.random.random((3, 1)))  # 3 x 1
	B = lndarray(np.random.random((1, 3)))  # 1 x 3
	C = lndarray(np.random.random((3, 5)))  # 3 x 5
	D_expected = np.matmul(A, np.matmul(B, C)) # 3 * 1 * 3 + 3 * 3 * 5 = 9 + 45 = 54 calculation
	D_actual = A.ldot(B).ldot(C) # currently lazy 
	D_actual = D_actual.eval() # should optimize A * (B * C) = 1 * 3 * 5 + 3 * 1 * 5 = 15 + 15 = 30 calculation
	assert D_actual.shape == D_expected.shape
	assert np.array_equal(D_actual, D_expected)