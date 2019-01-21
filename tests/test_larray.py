""" Test larray class """

import numpy as np

from lazynumpy.larray import lndarray


# pylint: disable=no-member
def assert_array_equal(actual, expected):
    """

    :param actual: actually returned
    :param expected: expected value
    :return: None
    """
    assert (np.abs(actual - expected) < np.finfo(float).resolution).all()
# pylint: enable=no-member


# pylint: disable=invalid-name, missing-docstring, assignment-from-no-return, too-many-function-args
def test_two_matrices():
    A = lndarray(np.random.random((3, 1)))
    B = lndarray(np.random.random((1, 3)))
    C_expected = A.dot(B)
    C_actual = A.ldot(B)  # currently lazy
    C_actual = C_actual.eval()  # get value
    assert C_actual.shape == C_expected.shape
    assert_array_equal(C_actual, C_expected)
# pylint: enable=assignment-from-no-return, too-many-function-args


def test_three_matrices():
    A = lndarray(np.random.random((3, 1)))  # 3 x 1
    B = lndarray(np.random.random((1, 3)))  # 1 x 3
    C = lndarray(np.random.random((3, 5)))  # 3 x 5
    D_expected = np.dot(A, np.dot(B, C))  # 3 * 1 * 3 + 3 * 3 * 5 = 9 + 45 = 54 calculation
    D_actual = A.ldot(B).ldot(C)  # currently lazy
    # should optimize A * (B * C) = 1 * 3 * 5 + 3 * 1 * 5 = 15 + 15 = 30 calculation
    D_actual = D_actual.eval()
    assert D_actual.shape == D_expected.shape
    assert_array_equal(D_actual, D_expected)


def test_on_d_matrice():
    A = lndarray(np.random.random((3, 1)))
    B = lndarray(np.random.random((1, 3)))
    C = lndarray(np.random.random((3,)))
    D_expected = np.dot(A, np.dot(B, C))  # 3 * 1 * 3 + 3 * 3 * 5 = 9 + 45 = 54 calculation
    D_actual = A.ldot(B).ldot(C)  # currently lazy
    # should optimize A * (B * C) = 1 * 3 * 5 + 3 * 1 * 5 = 15 + 15 = 30 calculation
    D_actual = D_actual.eval()
    assert D_actual.shape == D_expected.shape
    assert_array_equal(D_actual, D_expected)


def test_scalar():
    A = lndarray(np.random.random((3, 1)))
    B = lndarray(np.random.random((1, 3)))
    C = lndarray(3)
    D_expected = np.dot(A, np.dot(B, C))
    D_actual = A.ldot(B).ldot(C)
    D_actual = D_actual.eval()
    assert D_actual.shape == D_expected.shape
    assert_array_equal(D_actual, D_expected)

    A = lndarray(3)
    B = lndarray(np.random.random((3, 1)))
    C = lndarray(np.random.random((1, 3)))
    D_expected = np.dot(A, np.dot(B, C))
    D_actual = A.ldot(B)
    D_actual = D_actual.ldot(C)
    D_actual = D_actual.eval()
    assert D_actual.shape == D_expected.shape
    assert_array_equal(D_actual, D_expected)
# pylint: enable=invalid-name, missing-docstring

if __name__ == '__main__':
    test_scalar()
