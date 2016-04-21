import zen
import csv
import sys
sys.path.append('../zend3js/')
import d3js

#Query user on what gml file to generate

## Create the graph of interest
#acled_graph = zen.Graph()

#This function adds an edge if not present, adds weight if edge is present:
def add_weight(G,nodeA,nodeB,myValue):
	if G.has_edge(nodeA,nodeB):
		myWeight = G.weight(nodeA,nodeB)+myValue
		G.set_weight(nodeA,nodeB,myWeight)
	else:
		G.add_edge(nodeA,nodeB,weight=myValue)

#Reminder: Put the .csv source file in the SAME folder as this .py file
#'ACLED_all.csv'

class_Dict = {}

for i in range(0, 9):
    class_Dict[i] = []

with open('acled-2014-2015.csv') as mycsv:
	reader = csv.DictReader(mycsv)
	for row in reader:
		
		if not (row['ACTOR1'] in class_Dict[int(row['INTER1'])] ):
		    class_Dict[int(row['INTER1'])].append(row['ACTOR1'])
		
		if not (row['ACTOR2'] in class_Dict[int(row['INTER2'])] ):
		    class_Dict[int(row['INTER2'])].append(row['ACTOR2'])
		

def modularity(G,c):
	d = dict()
	for k,v in c.iteritems(): # for Key 'k' and Value 'v' in the dictionary 'c'
		for n in v: # for each node in the group 'k',
			d[n] = k # assign a group to the node 'n'
			# 'd' now becomes a dictionary {node1: class1, node2: class2 ...}
	
	Q, Qmax = 0,1
	
	# for all pairs of nodes,
	for u in G.nodes_iter():
		for v in G.nodes_iter():		    
			if d[u] == d[v]: # if the two nodes belong in the same class,
			    
			    # int(True) = 1, int(False) = 0
				Q += ( int(G.has_edge(v,u)) - G.degree(u)*G.degree(v)/float(G.num_edges) )/float(G.num_edges)
				Qmax -= ( G.degree(u)*G.degree(v)/float(G.num_edges) )/float(G.num_edges)
	return Q, Qmax


class_Dict.pop(0, None)

#G = zen.io.gml.read('acled1415graph(events).gml', weight_fxn=lambda x:x['weight'])
G = zen.io.gml.read('acled1415graph(fatalities).gml', weight_fxn=lambda x:x['weight'])

#testing = zen.algorithms.modularity(G, class_Dict, weighted=False)

Q, Qmax = modularity(G,class_Dict)
print 'Modularity (Countries): %1.4f / %1.4f\n' % (Q,Qmax)
print 'Normalised Modularity:", Q/Qmax
