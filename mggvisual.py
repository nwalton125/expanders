from mgg import *

G = make_expander(9)
nx.draw_spectral(G, node_size = 10, width = .1)
plt.show()