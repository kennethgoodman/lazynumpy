from collections import namedtuple
import random

def get_list_default(alist, index, default):
	try:
		return alist[index]
	except IndexError:
		return default

def compute_cost(*args):
	if len(args) == 1:
		return 0
	elif len(args) == 2:
		A, C = args
		B = A
	elif len(args) == 3:
		A, B, C = args
	else:
		raise ValueError("")
	if hasattr(A, 'width'):
		return A.width * B.height * C.height
	else:
		return get_list_default(A.shape, 0, 1) * get_list_default(B.shape, 1, 1) * get_list_default(C.shape, 1, 1)


def Cost(matrices, backtrack=False):
	""" min cost for computing Ai ... Aj """
	S = {}
	splits = {}
	for i, m in enumerate(matrices):
		S[(i, i)] = 0
	for s in range(len(matrices)):
		for i in range(len(matrices) - s):
			j = i + s
			for l in range(i, j):
				print(i,l,j, matrices)
				cost = compute_cost(matrices[i], matrices[l], matrices[j]) 
				cur = cost + S.get((i,l),float('inf')) + S.get((l+1, j),float('inf'))
				if cur < S.get((i,j),float('inf')):
					S[(i,j)] = cur
					splits[(i, j)] = l
	if backtrack:
		ordered_matrices = []
		split = splits[(0, len(matrices) - 1)]
		def create_it(start, end):
			if start == end:
				return [matrices[start]]
			elif end - start == 1:
				return matrices[start:end + 1]
			split = splits[(start, end)]
			return [create_it(start, split)] + [create_it(split + 1, end)]
		return create_it(0, len(matrices) - 1), S[(0, len(matrices) - 1)]
	else:
		return S[(0, len(matrices) - 1)]

def reduce_tree(el, mul_f):
	print(el)
	if isinstance(el, list) and not isinstance(el[0], list):
		last = el[0]
		for m in el[1:]:
			print('multiplying {} and {}'.format(last, m))
			last = mul_f(last, m)
			print('returned', last)
		return last 
	elif isinstance(el, list) and len(el) == 2:
		left = reduce_tree(el[0], mul_f)
		right = reduce_tree(el[1], mul_f)
		print('multiplying {} and {}'.format(left, right))
		a = mul_f(left, right)
		print('returned', a)
		return a
	else:
		return el