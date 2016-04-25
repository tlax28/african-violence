import zen
import numpy
import numpy.linalg as la

#G = zen.io.edgelist.read('LotR_characters.edgelist',weighted=True)
#G = zen.io.edgelist.read('hobbit_LotR_characters.edgelist',weighted=True)
G = zen.io.gml.read('ACLED_Graph_Events_1997_1997.gml', weight_fxn=lambda x:x['weight'])
A = G.matrix()
N = G.num_nodes

# prints the top five (num) nodes according to the centrality vector v
# v takes the form: v[nidx] is the centrality of node with index nidx
def print_top(G,v, num=5):
	idx_list = [(i,v[i]) for i in range(len(v))]
	idx_list = sorted(idx_list, key = lambda x: x[1], reverse=True)
	for i in range(min(num,len(idx_list))):
		nidx, score = idx_list[i]
		print '  %i. %s (%1.4f)' % (i+1,G.node_object(nidx),score)
		#print '  %i. %s' % (i+1,G.node_object(idx))

# returns the index of the maximum of the array
# if two or more indices have the same max value, the first index is returned
def index_of_max(v):
	return numpy.where(v == max(v))[0]
	
print '\n============================================='
# Degree Centrality
print '\nDegree Centrality:'

v=[]
G.compact()

v = [A[i].sum() for i in range(N)] 

print_top(G, v, num=20)


print '\n============================================='
# Eigenvector Centrality
print '\nEigenvector Centrality (by Zen):'

v = zen.algorithms.centrality.eigenvector_centrality_(G, weighted=True)
print_top(G, v, num=20)