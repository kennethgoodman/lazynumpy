""" file to hold internal _Evals class """

from lazynumpy.util import optimal_eval

# pylint: disable=fixme
class _Evals():
    """ Holds delayed evals """
    def __init__(self, val):
        if isinstance(val, list):
            self.vals = val
        else:
            self.vals = [val]

    def __mul__(self, other):
        # TODO: should we use extend instead so it overwrites the value in memory instead of a copy?
        return _Evals(self.vals + other.vals)

    def __call__(self):
        ordered_vals, _ = optimal_eval.get_cost(self.vals, backtrack=True)
        return_val = optimal_eval.reduce_tree(ordered_vals, lambda x, y: x.dot(y))
        self.vals = [return_val]
        return return_val
# pylint: enable=fixme
