import networkx as nx
import matplotlib.pyplot as plt
from magicalECCS import suff_small_sublists

#Returns all length k lists that are contained within a given list, such that list
#ordering is preserved and multiplicities count. That is, [0,1,2,3,4,5,6] appears twice in the 7-sublists of[0,1,2,3,4,5,6,6].
def k_sublists(l, k):
	if k == 0:
		return [[]]
	if len(l) < k:
		return []
	return (k_sublists(l[1:], k) + list(map(lambda s: [l[0]]+s, k_sublists(l[1:], k-1))))

#Finds the Cheeger constant of any graph (warning: my implementation is EXPTIME)
#The Cheeger constant of G is the minimum value of |dS| / |S|, over all node_sublists S of G with <= n/2 vertices. dS is the edge boundary of S. 
def cheeger_constant(G):
	num_nodes = len(G.nodes())
	node_sublists = suff_small_sublists(G.nodes(), num_nodes // 2)
	node_sublists.remove([])
	min_val = num_nodes - 1 #An upper bound on the minimum value of the edge boundary, but it's possible that no node attains this value. In the for loop, this value will be used for comparison.
	for sl in node_sublists:
		min_val = min(min_val, len(nx.edge_boundary(G, sl)) / len(sl))
	return min_val

"""
R = nx.fast_gnp_random_graph(10, .2)
print(R.nodes())
for i in range(10):
	print(R.neighbors(i))
print(nx.edge_boundary(R, [1,2,3]))
#nx.draw_circular(R)
#plt.show()
print(cheeger_constant(R))"""

f1, f2 = [experimental_cheeger_constant, cheeger_constant]

for n in range(1,14):
	print(n)
	G = nx.complete_graph(n)
	if n == 1:
		print(f1(G) == 0, f2(G) == 0)
	else:
		print(f1(G) == (n+1) // 2, f2(G) == (n+1) // 2)
	H = nx.cycle_graph(n)
	if n == 1:
		print(f1(H) == 0, f2(H) == 0)
	elif n == 2:
		print(f1(H) == 1, f2(H) == 1)
	if n > 2:
		print(f1(H) == 2 / (n//2), f2(H) ==  2 / (n//2))

for i in range(100):
	E = nx.erdos_renyi_graph(6, .7)
	if f1(E) != f2(E):
		print(f1(E), f2(E))
		nx.draw_circular(E)
		plt.show()



