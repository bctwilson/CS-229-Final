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

# Combine Tract Data for...:
# area, pop, lowinc, mins, under5, over64, age25up, laths, holds, lingoes,
# built units, pre1960, povknownratio, traffic.score

# For traffic.score: 
# In the case of census tract 6001400300, 
# the traffic.score = (1082*899+1203*181+1163*1238+1798*286) / (1082+1203+1163+1798).  What do you think?
# (sumWeightedTrafficScore/total_population)

# Small Detail: Some Census Tracts are missing!!! 

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
	"povknownratio", 
	"mins", 
	"under5", 
	"over64", 
	"age25up", 
	"lths", 
	"hhlds", 
	"lingiso", 
	"builtunits", 
	"pre1960", 
	"traffic.score"
	]

fieldsToUpdate = [
	"area", 
	"pop", 
	"lowinc", 
	"povknownratio", 
	"mins", 
	"under5", 
	"over64", 
	"age25up", 
	"lths", 
	"hhlds", 
	"lingiso", 
	"builtunits", 
	"pre1960", 
	"traffic.score"
]



numCensusTracts = 0
prev_tract = ""
rawEntriesToWrite_Dict = {} # These entries will have data lines from each census TRACT
rawEntriesToWrite = [] # These entries will have data lines from each census TRACT

def calculate_unknown_pov(row, longHeader):
	return int(row[longHeader.index("pop")]) - int(row[longHeader.index("povknownratio")])


def createNewEntry(row, tract, longHeader):
	newRawEntry = []
	for index in fieldIndex: # Write desired data into a python list. 
		newRawEntry.append(row[index]) 
	newRawEntry[1] = tract # Exclude last digit!!!
	newRawEntry[fieldsWanted.index("povknownratio")] =  calculate_unknown_pov(row, longHeader) # Actually want to keep track of number of unknown pov status
	print "New entry!: "
	print newRawEntry
	rawEntriesToWrite_Dict[tract] = newRawEntry

def updateTract(row, tract, longHeader):
	# Build a new entry. Take the values of the old entry, and add to the values, based on what was discussed. Then update dictionary key with
	# new entry 
	newEntry = rawEntriesToWrite_Dict[tract] # Copy old entry to this, to be updated, and then replace in dictionary
	for field in fieldsToUpdate:
		if (field == "povknownratio"): # You're actually updating # of unknown poverty status in your tract
		  curr_unknownPov = int(newEntry[fieldsWanted.index("povknownratio")])
		  newEntry[fieldsWanted.index("povknownratio")] = str(curr_unknownPov+calculate_unknown_pov(row, longHeader))
  	
  	rawEntriesToWrite_Dict[tract] = newEntry
  	print "Updated Tract: "
  	print newEntry


def getCensusTractFromList(row):
	FIPS = row[1]
	tract = FIPS[0:11] # Only take first 11 digits, exclude the block number
	return tract

def updateDictionary(row, longHeader):
	tract = getCensusTractFromList(row)
	if tract in rawEntriesToWrite_Dict.keys():
		updateTract(row, tract, longHeader) 
	else:
		createNewEntry(row, tract, longHeader)



# Get index of each field, from the first row
def getFieldIndex(row, fieldIndex):
	global longHeader
	shortHeader = [];
	longHeader = row; 
	for field in fieldsWanted:
		ind = row.index(field)
		fieldIndex.append(ind)
		shortHeader.append(row[ind])
	shortHeader[8] = "povUnknown"
	rawEntriesToWrite.append(shortHeader)
	print shortHeader
	return longHeader

def addEntry(row):
	updateDictionary(row) 



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

numLinesToOpen = 5
iterNum = 0
print "Reading File..."

with open('EJScreen_SocioDemographic_California_FIPS_Sorted.csv', 'rU') as f: 
    reader = csv.reader(f)
    fieldIndex = []
    longHeader = [];
    numCensusTracts = 0;
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
        	updateDictionary(row, longHeader)     
    	else:
    		longHeader = getFieldIndex(row, fieldIndex)
        iterNum +=1
print "Fileread Complete! \n"

print "Number of Census Tracts: %d " %(len(rawEntriesToWrite_Dict))

print "Now it's time to display dictionary... "



