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

selectByFatality = raw_input("Do you want to weigh the edges by count of events or fatalities? 1 for events, 2 for fatalities\n")

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

#Reminder: Put the .csv source file in the SAME folder as this .py file
#'acled-2014-2015.csv'

with open('ACLED_all.csv') as mycsv:
	reader = csv.DictReader(mycsv)
	for row in reader:
		#By default include row for processing
		to_process = True
		
		#Following statements change to_process depending on conditions
		
		if selectYear:
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
			if int(selectByFatality)==1:
				add_weight(acled_graph,row['ACTOR1'],row['ACTOR2'],1)
			else:
				deathCount = int(row['FATALITIES'])
				if deathCount > 0:
					add_weight(acled_graph,row['ACTOR1'],row['ACTOR2'],deathCount)
		else:
			fail_count += 1

print "Number of nodes:",acled_graph.num_nodes
#print fail_count

## ====================== Writing the .gml File ======================
## File will be created in the current working directory
fileName = "ACLED_Graph"
if int(selectByFatality)==1:
	fileName += "_Events"
else:
	fileName += "_Fatalities"

if selectYear:
	fileName += "_" + str(startYear) + "_" + str(endYear)

fileName += ".gml"

zen.io.gml.write(acled_graph, fileName)
print "GML file with the name", fileName, "has been created."

## ====================== Visualisation ======================

#d3 = d3js.D3jsRenderer(acled_graph, 
                        #event_delay=0.1, 
                        ##canvas_size = (1600,700), 
                        #interactive=False, 
                        #autolaunch=False)

#d3.update()

#d3.stop_server()

