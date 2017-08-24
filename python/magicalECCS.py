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







#TODO:
#-Make a magical graph and test this code. Something feels wrong about testing -- how do we know that it's *really* right?
#-Make a function that converts magical graphs into error correcting codes.

#Takes a magical graph and makes it into an error correcting code
#def magical_graph_to_ecc(G, L, R):

