import zen
import csv
import sys
sys.path.append('../zend3js/')
import d3js

#Reminder: Put the .csv source file in the SAME folder as this .py file
#'acled-2014-2015.csv'

def makeGraph(selectYear,selectByFatality,startYear=1997,endYear=2015):
	fail_count = 0
	## Create the graph of interest
	acled_graph = zen.Graph()

	#This function adds an edge if not present, adds weight if edge is present:
	def add_weight(G,nodeA,nodeB,myValue):
		if G.has_edge(nodeA,nodeB):
			myWeight = G.weight(nodeA,nodeB)+myValue
			G.set_weight(nodeA,nodeB,myWeight)
		else:
			G.add_edge(nodeA,nodeB,weight=myValue)

	with open('ACLED_all.csv') as mycsv:
		reader = csv.DictReader(mycsv)
		for row in reader:
			#By default include row for processing
			to_process = True
			
			#Following statements change to_process depending on conditions
			
			if selectYear != "Y":
				if int(row['YEAR'])> endYear or int(row['YEAR'])<startYear:
					to_process = False
			
			#Do not include if actor1/2 are "NA" (only two-parties please)
			if row['ACTOR1']== 'NA' or row['ACTOR2'] == 'NA' or row['ACTOR2'] =="":
				to_process = False
			
			#Do not include self-edges
			if row['ACTOR1']==row['ACTOR2']:
				to_process = False
			
			if to_process:
				#Add the edge
				if selectByFatality==1:
					add_weight(acled_graph,row['ACTOR1'],row['ACTOR2'],1)
				else:
					deathCount = int(row['FATALITIES'])
					if deathCount > 0:
						add_weight(acled_graph,row['ACTOR1'],row['ACTOR2'],deathCount)
			else:
				fail_count += 1

	print "Number of nodes in generated graph:",acled_graph.num_nodes
	#print fail_count
	
	return acled_graph

