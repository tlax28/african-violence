import zen
import csv
import sys
sys.path.append('../zend3js/')
import d3js

#Query user on what gml file to generate
selectYear = raw_input("Do you want to use all the data? Input Y/N\n")

if selectYear == "N":
	startYear = int(raw_input("Please input start year: (earliest possible is 1997)\n"))
	endYear = int(raw_input("Please input end year: (latest possible is 2015)\n"))
	selectYear = True
else:
	selectYear = False

## Create the graph of interest
acled_graph = zen.Graph()

#This function adds an edge if not present, adds weight if edge is present:
def add_weight(G,nodeA,nodeB,myValue):
	if G.has_edge(nodeA,nodeB):
		myWeight = G.weight(nodeA,nodeB)+myValue
		G.set_weight(nodeA,nodeB,myWeight)
	else:
		G.add_edge(nodeA,nodeB,weight=myValue)

fail_count = 0
#ALERT
#PUT THE .csv FILE IN THE SAME FOLDER AS THE .py FILE
#'ACLED_all.csv'
with open('acled-2014-2015.csv') as mycsv:
	reader = csv.DictReader(mycsv)
	for row in reader:
		#By default include row for processing
		to_process = True
		
		#Following statements change to_process depending on conditions
		
		if selectYear:
			if int(row['YEAR'])> endYear or int(row['YEAR'])<startYear:
				to_process = False
		
		#Do not include if actor1/2 are "NA" (only two-parties please)
		if row['ACTOR1']== 'NA' or row['ACTOR2'] == 'NA':
			to_process = False
		
		#Do not include self-edges
		if row['ACTOR1']==row['ACTOR2']:
			to_process = False
		
		if to_process:
			#Add graph
			add_weight(acled_graph,row['ACTOR1'],row['ACTOR2'],1)
		else:
			fail_count += 1

print acled_graph.num_nodes
print fail_count

## Referencing field entries
##ACTOR1
##ALLY_ACTOR_1
##ACTOR2
##ALLY_ACTOR_2
##FATALITIES


## ====================== Writing the .gml File ======================
## File will be created in the current working directory
#zen.io.gml.write(acled1415graph, "acled1415graph.gml")


## ====================== Visualisation ======================

#d3 = d3js.D3jsRenderer(acled_graph, 
                        #event_delay=0.1, 
                        ##canvas_size = (1600,700), 
                        #interactive=False, 
                        #autolaunch=False)

#d3.update()

#d3.stop_server()

