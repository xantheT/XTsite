import csv

#############################################################################
# This file takes in csv files of the same form as we use for strix, parses them
# and outputs a text string that can be read in by an html file. This html file
# then uses js to display the info contained our csvs in a rough visualization.
# Basically, it allows us to see the objects and their paths and move them about.
#############################################################################


#import / export files
crNodes = csv.reader(open("./nodes.csv","rb"))
crPaths = csv.reader(open("./paths.csv","rb"))
outFile = open('./pathsAndNodes.js', 'w')


###### sort out and format the nodes #########
incrementNo = 0
nodeDict = {}
for row in crNodes:
	if ( row[2]=='node.artifact' or row[2]=='node.journey-intro'):
		nodeDict[row[0]] = incrementNo
		incrementNo = incrementNo + 1

#change the dictionary into a sorted list, sorted by the value which is the entry number of the artifact.
#could have just had a list in the first place, but kep dict incase decide to use a dict type structure later.
sortedList = sorted(nodeDict.items(), key=lambda x: x[1]) 

#get into JSON format for the d3 javascript. Hacky - create a big string
# format = ' {"name":"<name of node>","group":1, "num":<order it appears in in the csv file>},  '
JSON_nodes = ""
for elem in sortedList:
	entry = '{"name":"'+elem[0]+'","group":1, "num":'+str(elem[1])+'},\n'
	JSON_nodes +=entry



########## sort out and format the paths ############

#create dictionary of paths, where the key is the journey and the values are an array 
#of the links within that journey
pathDict = {}
for row in crPaths:
	if row[2]=='TPGraphNetLink':
		stripped =row[0].lstrip('path.')
		tupl = stripped.partition('.')
		path = tupl[0]
		nodes = tupl[2].partition('-node.')
		nodePair = [nodes[0], 'node.'+nodes[2]]
		if path in pathDict:
			pathDict[path].append(nodePair)
		else:
			pathDict[path] = [nodePair]

#Now format the dictionary into the string that d3 wants :{"source":0,"target":2,"value":10}
# big string again.eek
# format = ' {"source":<num of from node>,"target":<num of to node>,"value":<path num>,"name":"look-to-the-stars"}, '
JSON_paths = ""
pathCounter = 0
for pathKey in pathDict:
	for tupleArr in pathDict[pathKey]:
		pathString = '{"source":'+str(nodeDict[tupleArr[0]])+',"target":'+str(nodeDict[tupleArr[1]])+',"value":'+str(pathCounter)+',"name":"'+pathKey+'"},\n'
		JSON_paths += pathString
	pathCounter = pathCounter + 1




####### write the completed node and path info to the .js file  ######
outFile.write("var importNodes =[\n"+JSON_nodes+" ];\n")
outFile.write("var importPaths = [\n"+JSON_paths+" ];\n")
outFile.close()
