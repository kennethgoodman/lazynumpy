""" testing lazynumpy.util.optimal_eval """

import random
from collections import namedtuple
import string

import pytest

from lazynumpy.util import optimal_eval


# pylint: disable=invalid-name,redefined-outer-name,missing-docstring
@pytest.fixture()
def Matrix():
    return namedtuple('Matrix', ['shape', 'name'])


def test_cost(Matrix):
    A = Matrix(shape=(3, 1), name='A')
    B = Matrix(shape=(1, 3), name='B')
    C = Matrix(shape=(3, 5), name='C')
    optimized = optimal_eval.get_cost([A, B, C])
    expected = 1 * 3 * 5 + 3 * 1 * 5  # A * (B * C)
    assert optimized == expected


def test_cost_backtracking(Matrix):
    A = Matrix(shape=(3, 4), name='A')
    B = Matrix(shape=(4, 3), name='B')
    C = Matrix(shape=(3, 14), name='C')
    D = Matrix(shape=(14, 3), name='D') # 3 * 4 * 3 + 3 * 3 * 14 + 3 * 14 * 3
    expected = 3 * 4 * 3 + 3 * 14 * 3 + 3 * 3 * 3  # (A * B) * (C * D)
    ordered, optimized = optimal_eval.get_cost([A, B, C, D], backtrack=True)  # ((A * B) * (C * D))
    assert optimized == expected
    assert ordered[0][0] == A
    assert ordered[0][1] == B
    assert ordered[1][0] == C
    assert ordered[1][1] == D


def test_reduce_tree(Matrix):
    A = Matrix(shape=(3, 1), name='A')
    B = Matrix(shape=(1, 3), name='B')
    C = Matrix(shape=(3, 5), name='C')
    ordered, _ = optimal_eval.get_cost([A, B, C], backtrack=True)
    reduce_f = lambda left, right: Matrix(shape=(left.shape[0], right.shape[1]),
                                          name='({} * {})'.format(left.name, right.name))
    reduced = optimal_eval.reduce_tree(ordered, reduce_f)
    assert reduced.shape == (3, 5) and reduced.name == '(A * (B * C))'


def test_always_minimized(Matrix):
    def get_new_matrix(last, name):
        return Matrix(shape=(last.shape[1], random.randint(1, 25)), name=name)

    for seed in range(3):
        random.seed(seed)
        for number_of_matrices in [2, 3, 10, 25]:
            matrices = [Matrix(shape=(random.randint(1, 25), random.randint(1, 25)), name='A')]
            for name in string.ascii_uppercase[1:]:
                if len(matrices) >= number_of_matrices:
                    break
                matrices.append(get_new_matrix(matrices[-1], name))
            minimized = optimal_eval.get_cost(matrices)
            regular = 0
            last = matrices[0]
            for m in matrices[1:]:
                regular += optimal_eval.compute_cost(last, m)
                last = Matrix(shape=(last.shape[0], m.shape[1]),
                              name='({} * {})'.format(last.name, m.name))
            assert minimized <= regular
# pylint: enable=invalid-name,redefined-outer-name,missing-docstring
