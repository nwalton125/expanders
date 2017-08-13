from networkx import neighbors

#Question: What are good design patterns for objects that have to satisfy a certain property? For instance, magical graphs. There's no intuitive way to make a graph and always have it be magical (unless there's some neat parametrization of them that I'm missing). You could just use a standard graph object and add an "is_magical" method. But I guess I want something more elegant. I don't know if this problem is solvable.

#Finds all sublists of our list, and multiplicities count and order is retained.
def sublists(l):
	if l == []:
		return [[]]
	smaller_sublists = sublists(l[1:])
	return smaller_sublists + list(map(lambda s: [l[0]] + s, smaller_sublists))

#Finds all sublists of l with at most k elements, where multiplicities count and order is retained.
def suff_small_sublists(l, k):
	if k < 0:
		return []
	elif l == [] or k == 0:
		return [[]]
	smaller_sublists = suff_small_sublists(l[1:], k)
	all_sublists = []
	for s in smaller_sublists:
		all_sublists.append(s)
		if len(s) < k:
			all_sublists.append([l[0]] + s)
	return all_sublists

#Given a subset S of vertices of G, finds the neighborhood of elements of S.
def nbhood(G, S):
	nbs = {}
	for v in S:
		for nb in G.neighbors(v):
			nbs[nb] = 0
	return list(nbs)


#Given are a d-regular bipartite graph G and it's left and right vertex sets. This functions (inefficiently) checks whether G is magical.
def is_magical(G, L, R, d):
	for sub_L in suff_small_sublists(L, n // 2):
		sub_L_nbs = nbhood(G, sub_L)
		if len(sub_L) <= n / (10 * d):
			if len(sub_L_nbs) < len(sub_L) * 5 * d / 8:
				return False
		else:
			if len(sub_L_nbs) < len(sub_L):
				return False
	return True


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







#TODO:
#-Make a magical graph and test this code. Something feels wrong about testing -- how do we know that it's *really* right?
#-Make a function that converts magical graphs into error correcting codes.

#Takes a magical graph and makes it into an error correcting code
#def magical_graph_to_ecc(G, L, R):

