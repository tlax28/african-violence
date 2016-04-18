import zen
import csv
import sys
sys.path.append('../zend3js/')
import d3js

# PUT THE .csv FILE IN THE SAME FOLDER AS THE .py FILE

acled1415file = csv.reader(open("acled-2014-2015.csv"))

# ====================== Importing the Raw File ======================

# Storing the values in the list 'acled1415'
acled1415 = []
for row in acled1415file:
    acled1415.append(row)

headers = acled1415[0] # the headers are in the first row

acled1415 = acled1415[1:] # removes the headers row

acled1415new = [] # This shall be a list of dictionaries

for entry in acled1415: # entry is the list of values in each row
    entrydict = {}
    for i in range(len(headers)):
        entrydict[headers[i]] = entry[i]  # keys are the header names and values are the corresponding data in the row
    acled1415new.append(entrydict)  


# ====================== Creating the Graph ======================

acled1415graph = zen.Graph()

for entry in acled1415new:
    # Each entry is a dictionary
    ACTOR1 = entry['ACTOR1']
    ACTOR2 = entry['ACTOR2']

    if ACTOR1 == 'NA' or ACTOR2 == 'NA': # if one of the actors is 'NA', then skip.
        break
        
    if acled1415graph.has_edge(ACTOR1, ACTOR2): # if edge already exists
        currentweight = acled1415graph.weight(ACTOR1, ACTOR2) # Take the cerrent weight of the edge
        acled1415graph.set_weight(ACTOR1, ACTOR2, currentweight+1) # And add 1 to it.
    
    else:    # if the edge doesn't yet exist
        acled1415graph.add_edge(ACTOR1, ACTOR2, weight=1) # add edge with weight 1

# ====================== Writing the .gml File ======================
# File will be created in the current working directory
zen.io.gml.write(acled1415graph, "acled1415graph.gml")


# ====================== Visualisation ======================

d3 = d3js.D3jsRenderer(acled1415graph, 
                        event_delay=0.1, 
                        #canvas_size = (1600,700), 
                        interactive=False, 
                        autolaunch=False)

d3.update()

d3.stop_server()

