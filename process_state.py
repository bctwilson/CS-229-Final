import csv
import numpy 

import matplotlib; matplotlib.use('Agg') # Use a backend that doesn't require a display.
import matplotlib.pyplot as plt # Use the pyplot interface of matplotlib.
import pickle 


# Reading File...
# 01047957300
# Previous tract:
# 01047956400
# Previous tract:01047957300
# 01047956202
# Previous tract:01047956400
# 01047956900
# Previous tract:01047956202
# 01047956201
# Previous tract:01047956900
# 01047956900
# Previous tract:01047956201
# 01047957200
# Previous tract:01047956900
# 01047956400
# Previous tract:01047957200
# 01047957300
# Previous tract:01047956400
# Fileread Complete! 

# Number of census tracts in California: 9

fieldsWanted = [
	"OBJECTID", 
	"FIPS", 
	"ST",  
	"statename", 
	"REGION", 
	"area", 
	"pop", 

	"lowinc", 
	"pctlowinc", 
	"pctile.pctlowinc", 
	"povknownratio", 

	"mins", 
	"pctmin", 
	"pctile.pctmin", 


	"under5", 
	"pctunder5", 
	"pctile.pctunder5", 

	"over64", 
	"pctover64", 
	"pctile.pctover64", 

	"age25up", 
	"lths", 
	"pctlths", 
	"pctile.pctlths", 

	"hhlds", 
	"lingiso", 
	"pctlingiso", 
	"pctile.pctlingiso", 

	"builtunits", 
	"pre1960", 
	"pctpre1960", 
	"pctile.pctpre1960", 

	"traffic.score", 
	"pctile.traffic.score", 
	]



global prev_tract, numCensusTracts

numCensusTracts = 0
prev_tract = ""

def getCurrTract(FIPS_str):
	global prev_tract, numCensusTracts
	tractStr = FIPS_str[0:11]; # Only take first 11 digits, exclude the block number
	print tractStr	
	print "Previous tract:" + prev_tract
	if (tractStr != prev_tract):
		numCensusTracts +=1
		prev_tract = tractStr
	return tractStr

def getCensusTractFromList(entry):
	FIPS = entry[1]
	tract = FIPS[0:11]

# currTract = getCurrTract(row[1]); # Get current census tract (11-digits)

# print "Number of census tracts in California: %d" %numCensusTracts

# CODE TO SORT BELOW:::: 
# pkl_file = "California_SocioDemoGraphic_Lists.pkl"
# print "Loading file...."
# with open(pkl_file,'rb') as f:
# 	CaliforniaList = pickle.load(f) # This has a list of Huffman Objects that will be used as static hufffman tables. 
# 	f.close()
# print "Loaded!"

# # Sort the entries
# CaliforniaListSorted = sorted(CaliforniaList[1:len(CaliforniaList)-1], key=lambda entry: int(entry[1]))
# CaliforniaListSorted.insert(0,CaliforniaList[0])

# print "Writing to CSV File...."
# outFileName = "EJScreen_SocioDemographic_California_FIPS_Sorted.csv"
# with open(outFileName, "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(CaliforniaListSorted)
#     f.close()
# print "Write complete!"

numLinesToOpen = 10
iterNum = 0
print "Reading File..."

with open('EJScreen_SocioDemographic_California_FIPS_Sorted.csv', 'rU') as f: 
    reader = csv.reader(f)
    fieldIndex = []
    numCensusTracts = 0;
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	print row
    	print "\n"
        iterNum +=1
print "Fileread Complete! \n"