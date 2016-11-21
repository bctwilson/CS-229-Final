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
noTrafficTracts = []
noPopulationTracts = []

def getCensusTractFromList(row):
	FIPS = row[1]
	tract = FIPS[0:11] # Only take first 11 digits, exclude the block number
	return tract

def calculate_unknown_pov(row, longHeader):
	return int(row[longHeader.index("pop")]) - int(row[longHeader.index("povknownratio")])

def calculate_weighted_traffic_score(row, longHeader):
	if (row[longHeader.index("traffic.score")] != "NA"):
		return float(row[longHeader.index("pop")])*float(row[longHeader.index("traffic.score")])
	else:
		if (getCensusTractFromList(row) not in noTrafficTracts):
			noTrafficTracts.append(getCensusTractFromList(row))
		return 0

def createNewEntry(row, tract, longHeader):
	newRawEntry = []
	for index in fieldIndex: # Write desired data into a python list. 
		val = row[index]
		if (longHeader[index] in fieldsToUpdate): # Make them doubles
			if (longHeader[index] == "traffic.score"):
				newRawEntry.append(calculate_weighted_traffic_score(row, longHeader));
			else:
				newRawEntry.append(float(val))
		else:
			newRawEntry.append(val) 
	newRawEntry[1] = tract # Exclude last digit!!!
	newRawEntry[fieldsWanted.index("povknownratio")] =  calculate_unknown_pov(row, longHeader) # Actually want to keep track of number of unknown pov status
	# print "New entry!: "
	# print newRawEntry
	rawEntriesToWrite_Dict[tract] = newRawEntry

def updateTract(row, tract, longHeader):
	# Build a new entry. Take the values of the old entry, and add to the values, based on what was discussed. Then update dictionary key with
	# new entry 
	newEntry = rawEntriesToWrite_Dict[tract] # Copy old entry to this, to be updated, and then replace in dictionary
	for field in fieldsToUpdate:
		if (field == "povknownratio"): # You're actually updating # of unknown poverty status in your tract
		  curr_unknownPov = int(newEntry[fieldsWanted.index(field)])
		  newEntry[fieldsWanted.index(field)] = curr_unknownPov+calculate_unknown_pov(row, longHeader)
		elif (field == "traffic.score"):
			newEntry[fieldsWanted.index(field)] += calculate_weighted_traffic_score(row, longHeader)
		else:
			newEntry[fieldsWanted.index(field)] += float(row[longHeader.index(field)])
  	
  	rawEntriesToWrite_Dict[tract] = newEntry
  	# print "Updated Tract: "
  	# print newEntry


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
	rawEntriesToWrite.append(shortHeader)
	print shortHeader
	return longHeader

def addEntry(row):
	updateDictionary(row) 

def isPopulated(newEntry, tract):
	if (newEntry[fieldsWanted.index("pop")] != 0):
		return True
	else:
		if (tract not in noPopulationTracts):
			noPopulationTracts.append(tract)
		return False 




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

numLinesToOpen = -1
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


for key in rawEntriesToWrite_Dict:
	newEntry = rawEntriesToWrite_Dict[key]
	newEntry[fieldsWanted.index("povknownratio")] = (newEntry[fieldsWanted.index("pop")] - newEntry[fieldsWanted.index("povknownratio")] )
	if (key not in noTrafficTracts and isPopulated(newEntry,key)):
		newEntry[fieldsWanted.index("traffic.score")] = newEntry[fieldsWanted.index("traffic.score")]/newEntry[fieldsWanted.index("pop")]
	else: 
		newEntry[fieldsWanted.index("traffic.score")] = "NA"
	rawEntriesToWrite.append(newEntry)

# Sort the entries
rawEntriesToWrite_Sorted = sorted(rawEntriesToWrite[1:len(rawEntriesToWrite)], key=lambda entry: int(entry[1]))
rawEntriesToWrite_Sorted.insert(0,rawEntriesToWrite[0])

print "Writing to CSV File...."
outFileName = "EJScreen_SocioDemographic_California_FIPS_TRACTS_Sorted.csv"
with open(outFileName, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(rawEntriesToWrite_Sorted)
    f.close()
print "Write complete! \n"


print "No Traffic Data for the following tracts:"
for tract in noTrafficTracts: print tract
print "\n"
print "No Population Data for the following tracts:"
for tract in noPopulationTracts: print tract

# FINALLY, KEEP RUNNING SUM OF WEIGHTED TRAFFIC SUM. AND THEN DIVIDE BY POPULATION FOR EACH CENSUS TRACT TO GET TRAFFIC. 
# ALSO, KEEP RUNNING SUM OF NUMBER OF UNKNOWN POVERTY STATUS CALCULATION, SO YOU CAN DO FINAL CALCULATION IN THE END 


