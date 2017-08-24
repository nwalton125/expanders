#Finds the dot product of two equi-dimensional vectors.
def dot_F2(v, w):
	return sum([v[i] * w[i] for i in range(len(v))]) % 2

#Computes Av in the field with two elements.
def matmul_F2(A, v):
	return [dot_F2(arow, v) for arow in A] 

def concatenate_to_all(start, listofls):
	return [start + l for l in listofls]

#Suppose w is a row vector over F2, and k is a scalar in F2. This finds all column vectors that satisfy w*v = k.
def vecsolve_F2(w, k):
	if len(w) == 1:
		if w[0] == 0:
			return [[0],[1]]
		else:
			return [[k]]
	#Safety case
	if w == []:
		Raise("vectors can't be length zero")
	#subresult0 is the solution to the vector equation for w[1:] assuming w[0] * v[0] = 0
	subresult0 = vecsolve_F2(w[1:], k)
	if w[0] == 0:
		return concatenate_to_all([0], subresult0) + concatenate_to_all([1], subresult0)
	else:
		#subresult1 is the solution to the vector equation for w[1:]assuming w[0] * v[0] = 0
		subresult1 = vecsolve_F2(w[1:], (k-1) % 2)
		return concatenate_to_all([0], subresult0) + concatenate_to_all([1], subresult1)

#Finds the set of all elements v such that A*v equals b.
def matsolve_F2(A, b):
	candidates = vecsolve_F2(A[0], b[0])
	for i in range(1, len(A)):
		candidates = list(filter(lambda x: dot_F2(A[i], x) == b[i], candidates))
	return candidates


def kernel_F2(A):
	return matsolve_F2(A,[0 for i in range(len(A))])
