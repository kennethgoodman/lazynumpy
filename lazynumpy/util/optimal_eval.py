from collections import namedtuple
import random


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
		return A.shape[0] * B.shape[1] * C.shape[1]


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

def main(number_of_matrices = 8):
	def get_new_matrix(last):
		return Matrix(width=last.height, height=random.randint(1, 25))
	Matrix = namedtuple('Matrix', ['shape', 'name'])
	A = Matrix(shape=(3,4), name='A')
	B = Matrix(shape=(4,3), name='B')
	C = Matrix(shape=(3,14), name='C')
	D = Matrix(shape=(14,3), name='D')
	tree, cost = Cost([A,B,C,D], backtrack=True)
	print(tree)
	def reduce_tree(el):
		if isinstance(el, list) and not isinstance(el[0], list):
			last = el[0]
			for m in el[1:]:
				last = Matrix(shape=(last.shape[0],m.shape[1]), name='({} * {})'.format(last.name, m.name))
			return last 
		elif isinstance(el, list) and len(el) == 2:
			left = reduce_tree(el[0])
			right = reduce_tree(el[1])
			return Matrix(shape=(left.shape[0],right.shape[1]), name='({} * {})'.format(left.name, right.name))
		else:
			return el
	print(reduce_tree(tree))

	A = Matrix(width=3, height=1)
	B = Matrix(width=1, height=3)
	C = Matrix(width=3, height=5)
	print(Cost([A,B,C]))

	matrices = [Matrix(width=random.randint(1, 25), height=random.randint(1, 25))]
	print(matrices[-1])
	for i in range(number_of_matrices - 1):
		matrices.append(get_new_matrix(matrices[-1]))
		print(matrices[-1])
	minimized = C(matrices)
	regular = 0
	last = matrices[0]
	for m in matrices[1:]:
		regular += compute_cost(last, m)
		last = Matrix(width=last.width, height=m.height)
	print(minimized, regular)

if __name__ == '__main__':
	main()