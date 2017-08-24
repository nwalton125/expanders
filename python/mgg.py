import networkx as nx
import matplotlib.pyplot as plt

#It may be useful to test this function against margulis_gabber_galil_graph from networkx.

#Finds the labels of the neighbors of vertex v, assuming v is in Z_n * Z_n
#and part of a Margulis-Gabber-Galil graph.
def mgg_neighbors(v, n):
    x = v[0]
    y = v[1]
    nbs = [(x+2*y, y), (x-2*y, y), (x+2*y+1, y), (x-2*y-1, y), (x, y+2*x), (x, y-2*x), (x, y+2*x+1), (x,y-2*x-1)]
    return list(set(filter(lambda x: x != v, map(lambda x: (x[0]%n, x[1]%n), nbs))))

#Creates a Margulis-Gabber-Galil graph on Z_n * Z_n
def make_expander(n):
	G = nx.Graph()
	for x in range(n):
		for y in range(n):
			G.add_node((x,y))
			for nb in mgg_neighbors((x,y), n):
				G.add_edge((x,y), nb)
	return G

