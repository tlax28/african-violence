import zen
import csv
import sys
sys.path.append('../zend3js/')
import d3js
from acled_makeGraph import *
sourceFile = "acled-all-clean-hell.csv"
import pprint

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

### Following code prepares a dictionary of actor category values for later use
class_Dict = {}
with open(sourceFile) as mycsv:
	reader = csv.DictReader(mycsv)
	for row in reader:
		if row['ACTOR1'] in class_Dict:
			pass
		else:
			class_Dict[row['ACTOR1']]=row['INTER1']
		
		if row['ACTOR2'] in class_Dict:
			pass
		else:
			class_Dict[row['ACTOR2']]=row['INTER2']
		
		#if not (row['ACTOR1'] in class_Dict[int(row['INTER1'])] ):
		    #class_Dict[int(row['INTER1'])].append(row['ACTOR1'])
		
		#if not (row['ACTOR2'] in class_Dict[int(row['INTER2'])] ):
		    #class_Dict[int(row['INTER2'])].append(row['ACTOR2'])


### Following code prepares a dictionary of actor category values for later use
country_Dict = {}

country_Dict2 = {}
with open(sourceFile) as mycsv:
	reader = csv.DictReader(mycsv)
	for row in reader:
		if row['ACTOR1'] in country_Dict:
			#Check for conflicts
			if row['COUNTRY'] in country_Dict[row['ACTOR1']]:
				#There's no conflict!
				pass
			else:
				country_Dict[row['ACTOR1']].append(row['COUNTRY'])
				#print row['ACTOR1'], country_Dict[row['ACTOR1']]
		else:
			country_Dict[row['ACTOR1']]=[row['COUNTRY']]
		
		if row['ACTOR2'] in country_Dict2:
			#Check for conflicts
			if row['COUNTRY'] in country_Dict2[row['ACTOR2']]:
				#There's no conflict!
				pass
			else:
				country_Dict2[row['ACTOR2']].append(row['COUNTRY'])
				#print row['ACTOR2'], country_Dict[row['ACTOR2']]
		else:
			country_Dict2[row['ACTOR2']]=[row['COUNTRY']]
	print "Country generation complete!"

## Quick check of country dictionary
myC = 0
for key in country_Dict.keys():
	if len(country_Dict[key])>1:
		#to try and process these issues manually
		if " of " in key:
			if "Government of" in key or "Police Forces of" in key or "Military Forces of" in key:
				if key.find("(") == -1:
					myName = key[(key.find(" of ")+4):]
				else:
					myName = key[(key.find(" of ")+4):key.find(" (")]
				#print "\nNew:" , myName, "\nOld:", key
				country_Dict[key] = myName
		elif key.find("(") != -1:
			myName = key[(key.find("(")+1):(key.find(")"))]
			print "\nNew:" , myName, "\nOld:", key
		myC += 1
		#print myC, key, country_Dict[key]


		#if not (row['ACTOR1'] in class_Dict[int(row['INTER1'])] ):
		    #class_Dict[int(row['INTER1'])].append(row['ACTOR1'])
		
		#if not (row['ACTOR2'] in class_Dict[int(row['INTER2'])] ):
		    #class_Dict[int(row['INTER2'])].append(row['ACTOR2'])
		
		
### Following modularity function is adapted from Module 4
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


def size_of_Dict(myDict):
	myCount = 0
	for key in myDict:
		myCount += len(myDict[key])
	return myCount

print len(class_Dict.keys())

#G = zen.io.gml.read('acled1415graph(events).gml', weight_fxn=lambda x:x['weight'])
#G = zen.io.gml.read('acled1415graph(fatalities).gml', weight_fxn=lambda x:x['weight'])
#print G.num_nodes

#G = makeGraph("Y",2,0,0)
#print G.num_nodes

#G = makeBattleGraph("Y",2,0,0)
#print G.num_nodes

#### Generating the actual class dictionaries for use
#new_class_dict = {}
#for i in range(1,9):
	#new_class_dict[i] = []

#for myNode in G.nodes():
	#if int(class_Dict[myNode])==8:
		#G.rm_node(myNode)
	#else:
		#new_class_dict[int(class_Dict[myNode])].append(myNode)

##pprint.pprint(new_class_dict)

#### Now for actual modularity calculations
#print "\n=====================\n"

#testQ = zen.algorithms.modularity(G, new_class_dict, weighted=False)
#Q, Qmax = modularity(G,new_class_dict)
#print testQ
#print Q
#print 'Modularity (Countries): %1.4f / %1.4f' % (Q,Qmax)
#print 'Normalised Modularity:', Q/Qmax
