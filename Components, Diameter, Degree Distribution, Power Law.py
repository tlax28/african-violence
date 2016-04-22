# -*- coding: utf-8 -*-
# Clement Tan + Yeow Lih Wei， 1000948 + 1000974， 
# Section 2 (Monday and Wednesday mornings) 
# Module 4: Large-Scale Properties

import zen
import matplotlib.pyplot as plt  	# if matplotlib doesn't work comment this line out
plt.ioff()							# if matplotlib doesn't work comment this line out
from numpy import *
import sys
sys.path.append('../zend3js/')
import d3js
from time import sleep
import random

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
				Q += ( int(G.has_edge(v,u)) - G.degree(u)*G.degree(v)/(2*float(G.num_edges)) )/ (2*float(G.num_edges))
				Qmax -= ( G.degree(u)*G.degree(v)/(2*float(G.num_edges)) )/(2*float(G.num_edges))
	return Q, Qmax


## Plots the degree distribution and calculates the power law coefficent
def calc_powerlaw(G, kmin):
	ddist = zen.degree.ddist(G,normalize=False)
	
	#v = [A[i].sum() for i in range(N)] 
	#H=histogram(v, bins=max(v)-1)
	#ddist = H[0]

	cdist = zen.degree.cddist(G,inverse=True)
	k = arange(len(ddist)) #numpy.arange returns an array. Similar to range()
	
	# *******************************************
	# if matplotlib doesn't work comment this section out
	plt.figure(figsize=(8,12))
	plt.subplot(211)
	plt.bar(k, ddist, width=0.8, bottom=0, color='b')
	
	plt.subplot(212)
	plt.loglog(k, cdist)
	plt.hold(True)
	plt.plot([kmin, kmin], [0.00001, 1])
	plt.hold(False)

	# *******************************************
	# if matplotlib doesn't work, use this instead to export values to excel for plotting
	# list2csv(ddist,'filename.csv')
	
	N = float(G.num_nodes) * cdist[kmin] # number of nodes with degree greater than or equal to k_min
	
	sum_term = 0
	
	for node in G.nodes():
	    if G.degree(node) >= kmin:
	        sum_term += log(G.degree(node)/(kmin-0.5))
	
	alpha = 1 + N/sum_term # calculate using (8.6)!
	sigma = (alpha - 1) / sqrt(N) # calculate using (8.7)!
	print '%1.2f +/- %1.2f' % (alpha,sigma)
	#print '%i, %1.2f,  %1.2f' % (kmin, alpha,sigma)
	plt.show()

# SET THE GRAPH HERE =====================================
G = zen.io.gml.read('acled1415graph(events).gml', weight_fxn=lambda x:x['weight'])
#G = zen.io.gml.read('acled1415graph(fatalities).gml', weight_fxn=lambda x:x['weight'])


# FIND COMPONENTS ========================================
components = zen.algorithms.components(G)   # returns a list of components, each component is a (set) of nodes in the component

component_sizes = [len(component) for component in components]
print "Size of largest component:" , max(component_sizes)


## DIAMETER =============================================== WARNING! TAKES SUPER LONG.
#print "\nDiameter:", zen.diameter(G) 

## POWER LAW ==============================================
calc_powerlaw(G, 0)  # need to change kmin appropriately
