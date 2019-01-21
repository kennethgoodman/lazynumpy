""" Example script to show speedup """

import time

import numpy as np

from lazynumpy.larray import lndarray

# pylint: disable=missing-docstring,invalid-name,unexpected-keyword-arg,line-too-long
def timeit(method):
    """ https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d """
    def timed(*args, **kw):
        time_start = time.time()
        result = method(*args)
        time_start = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((time_start - time_start) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (time_start - time_start) * 1000))
        return result
    return timed


@timeit
def run_traditional_operations(matrices):
    rtn = matrices[0]
    for matrix in matrices[1:]:
        rtn = np.dot(rtn, matrix)
    return rtn


@timeit
def run_without_lndarray_but_with_knowledge(matrices):
    return np.dot(matrices[0], np.dot(matrices[1], matrices[2]))


@timeit
def run_with_lndarray(matrices):
    initial = lndarray(matrices[0])
    for matrix in matrices[1:]:
        matrix = lndarray(matrix)
        initial = initial.ldot(matrix)
    return initial.eval()


def main():
    np.random.seed(1)
    dimensions = 10_000
    A = lndarray(np.random.random((dimensions, 1)))
    B = lndarray(np.random.random((1, dimensions)))
    C = lndarray(np.random.random((dimensions, dimensions)))

    logtime_data = {}
    run_traditional_operations([A, B, C], logtime_data=logtime_data)
    run_without_lndarray_but_with_knowledge([A, B, C], logtime_data=logtime_data)
    run_with_lndarray([A, B, C], logtime_data=logtime_data)
    print(logtime_data)
# pylint: enable=missing-docstring,invalid-name,unexpected-keyword-arg,line-too-long


if __name__ == '__main__':
    main()
