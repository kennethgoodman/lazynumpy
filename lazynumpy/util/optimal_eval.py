""" functions to help compute optimal way to do operations """

from functools import reduce


def get_list_default(alist, index, default):
    """
    Works similar to dict.get(key, default) but for a list

    :param alist: the list to get from
    :param index: the index to get
    :param default: the default value if this index > len(alist)
    :return: value at that index or default
    """
    try:
        return alist[index]
    except IndexError:
        return default


def compute_cost(*args):
    """
    Computes the cost of multiplying matrices
    :param args: argument variable number of matrices
    :return: the cost
    """
    if len(args) == 1:
        return 0

    if len(args) == 2:
        first_element, last_element = args
        middle_element = first_element
    elif len(args) == 3:
        first_element, middle_element, last_element = args
    else:
        raise ValueError("")

    if hasattr(first_element, 'width'):
        return first_element.width * middle_element.height * last_element.height
    return get_list_default(first_element.shape, 0, 1) \
           * get_list_default(middle_element.shape, 1, 1) \
           * get_list_default(last_element.shape, 1, 1)


def get_cost(matrices, backtrack=False):
    """
    min cost for computing Ai ... Aj

    :param matrices: the matrices to optimize
    :param backtrack: should a tree of the optimal associative paranthesis should be returned
    :return: optimal cost + tree if backtrack=True
    """
    solution_dict = {}
    splits = {}
    for start_idx, _ in enumerate(matrices):
        solution_dict[(start_idx, start_idx)] = 0
    for idx in range(len(matrices)):
        for start_idx in range(len(matrices) - idx):
            end_idx = start_idx + idx
            for split_idx in range(start_idx, end_idx):
                cost = compute_cost(matrices[start_idx], matrices[split_idx], matrices[end_idx])
                cur = cost + solution_dict.get((start_idx, split_idx), float('inf')) + \
                             solution_dict.get((split_idx + 1, end_idx), float('inf'))
                if cur < solution_dict.get((start_idx, end_idx), float('inf')):
                    solution_dict[(start_idx, end_idx)] = cur
                    splits[(start_idx, end_idx)] = split_idx
    if backtrack:
        def create_it(start, end):
            if start == end:
                return [matrices[start]]

            if end - start == 1:
                return matrices[start:end + 1]
            split = splits[(start, end)]
            return [create_it(start, split)] + [create_it(split + 1, end)]

        return create_it(0, len(matrices) - 1), solution_dict[(0, len(matrices) - 1)]
    return solution_dict[(0, len(matrices) - 1)]


def reduce_tree(element, mul_f):
    """
    :param element: The root element
    :param mul_f: the function used to reduce two elements
    :return: the value after all operations
    """
    if isinstance(element, list) and not isinstance(element[0], list):
        return reduce(mul_f, element)
    left = reduce_tree(element[0], mul_f)
    right = reduce_tree(element[1], mul_f)
    return mul_f(left, right)
