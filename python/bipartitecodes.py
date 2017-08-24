import networkx as nx
import random
import matplotlib.pyplot as plt
import matrixfuncs as matfun
from math import log

#Creates a random bipartite graph with l nodes on the left and r on the right, and probability p for each edge existing.
def rand_bipartite_graph(l, r, p):
	G = nx.Graph()
	for n in range(l+r):
		G.add_node(n)
	for i in range(l):
		for j in range(r):
			if random.random() < p:
				G.add_edge(i,l+j)
	return G

#Returns a special type of adjacency matrix for bipartite graphs. Rows are indexed by the left set, columns by the right set. A cell is 1 iff an edge is present and 0 otherwise.
def bipartite_adj_mat(G, L, R):
	return [[int(G.has_edge(L[i], R[j])) for j in range(len(R))] for i in range(len(L))]

#Given a bipartite graph G with left and right edge sets L and R and prespecified, this function finds the corresponding error correcting code.
def bipartite_code(G, L, R):
	return matfun.kernel_F2(bipartite_adj_mat(G, L, R))

#Finds the rate of the code, as defined here http://www.cs.huji.ac.il/~nati/PAPERS/expander_survey.pdf . The input to this function is a list of equal length lists.
def code_rate(code):
	return log(len(code), 2) / len(code[0])

#Finds the Hamming distance between two equal length lists of binary numbers.
def hamming_dist(l1, l2):
	return sum([l1[i] != l2[i] for i in range(len(l1))])

#Returns the minimum Hamming distance between two codewords over all codewords. If there is just one codeword, returns the length of that codeword.
def code_dist(code):
	min_dist = len(code[0])
	for i in range(len(code)):
		for j in range(i+1, len(code)):
			min_dist = min(min_dist, hamming_dist(code[i],code[j]))
	return min_dist


ln = 20
rn = 15

for n in range(1,10):
	prob = n/10
	for it in range(100):
		G = rand_bipartite_graph(ln,rn,prob)
		bpc = bipartite_code(G, range(ln), range(ln, ln+rn))
		if len(bpc) > 20 and code_dist(bpc) > 2:
			print(G.nodes(), G.edges(), bpc)
