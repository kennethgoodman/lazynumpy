from collections import namedtuple
import pytest

from lazynumpy.util import optimal_eval 


@pytest.fixture()
def Matrix():
	return namedtuple('Matrix', ['shape', 'name'])


def test_cost(Matrix):
	A = Matrix(shape=(3,1), name='A')
	B = Matrix(shape=(1,3), name='B')
	C = Matrix(shape=(3,5), name='C')
	optimized = optimal_eval.Cost([A, B, C])
	expected = 1 * 3 * 5 + 3 * 1 * 5  #  A * (B * C)
	assert optimized == expected


def test_cost_backtracking(Matrix):
	A = Matrix(shape=(3,4), name='A')
	B = Matrix(shape=(4,3), name='B')
	C = Matrix(shape=(3,14), name='C')
	D = Matrix(shape=(14,3), name='D')
	regular  = 3 * 4 * 3   +    3 * 3 * 14    +   3 * 14 * 3
	expected = 3 * 4 * 3   +    3 * 14 * 3    +   3 * 3 * 3  #  (A * B) * (C * D)
	ordered, optimized = optimal_eval.Cost([A, B, C, D], backtrack=True) # ((A * B) * (C * D))
	assert optimized == expected
	assert ordered[0][0] == A
	assert ordered[0][1] == B
	assert ordered[1][0] == C
	assert ordered[1][1] == D


def test_reduce_tree(Matrix):
	A = Matrix(shape=(3,1), name='A')
	B = Matrix(shape=(1,3), name='B')
	C = Matrix(shape=(3,5), name='C')
	ordered, _ = optimal_eval.Cost([A, B, C], backtrack=True)
	reduce_f = lambda left, right: Matrix(shape=(left.shape[0], right.shape[1]), name='({} * {})'.format(left.name, right.name))
	reduced = optimal_eval.reduce_tree(ordered, reduce_f)
	assert reduced.shape == (3,5) and reduced.name == '(A * (B * C))'


if __name__ == '__main__':
	print(test_cost())
	print(test_cost_backtracking())
	print(test_reduce_tree())