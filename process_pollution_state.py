import csv
import numpy 

import matplotlib; matplotlib.use('Agg') # Use a backend that doesn't require a display.
import matplotlib.pyplot as plt # Use the pyplot interface of matplotlib.
import pickle 
import os



fieldsWanted = [
	"OBJECTID", 
	"FIPS", 
	"ST",  
	"statename", 
	"REGION", 
	"area", 
	"pop", 

	"builtunits", 
	"pre1960", 
	"o3", 
	"pm", 
	"proximity.npdes", 
	"proximity.npl", 
	"proximity.rmp", 
	"proximity.tsdf", 
	"traffic.score", 
]


fieldsToUpdate = [
	"area", 
	"pop", 
	"builtunits", 
	"pre1960", 
	"o3", 
	"pm", 
	"proximity.npdes", 
	"proximity.npl", 
	"proximity.rmp", 
	"proximity.tsdf", 
	"traffic.score", 
]

weightedFields = [
	"pm", 
	"o3",
	"proximity.npdes", 
	"proximity.npl", 
	"proximity.rmp", 
	"proximity.tsdf", 
	"traffic.score", 
]

AK_HI_fields = [
	"proximity.npdes", 
	"proximity.npl", 
	"proximity.rmp", 
	"proximity.tsdf", 
	"traffic.score"
	]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

def getStateName(filename):
	for statename in states:
		if (statename in filename and statename not in statelist):
			return statename

def getCensusTractFromList(row):
	FIPS = row[1]
	tract = FIPS[0:11] # Only take first 11 digits, exclude the block number
	return tract

def calculate_weighted_score(row, longHeader, field):
	if (row[longHeader.index(field)] != "NA"):
		return float(row[longHeader.index("pop")])*float(row[longHeader.index(field)])
	else:
		if (getCensusTractFromList(row) not in incompleteTracts):
			incompleteTracts.append(getCensusTractFromList(row))
		return 0

def createNewEntry(row, tract, longHeader):
	newRawEntry = []
	for index in fieldIndex: # Write desired data into a python list. 
		val = row[index]
		if (longHeader[index] in fieldsToUpdate): # Make them doubles
			if (longHeader[index] in weightedFields):
				newRawEntry.append(calculate_weighted_score(row, longHeader, longHeader[index]));
			else:
				newRawEntry.append(float(val))
		else:
			newRawEntry.append(val) 
	newRawEntry[1] = tract # Exclude last digit!!!
	# print "New entry!: "
	# print newRawEntry
	rawEntriesToWrite_Dict[tract] = newRawEntry

def updateTract(row, tract, longHeader):
	# Build a new entry. Take the values of the old entry, and add to the values, based on what was discussed. Then update dictionary key with
	# new entry 
	newEntry = rawEntriesToWrite_Dict[tract] # Copy old entry to this, to be updated, and then replace in dictionary
	for field in fieldsToUpdate:
		if (field in weightedFields):
			newEntry[fieldsWanted.index(field)] += calculate_weighted_score(row, longHeader, field)
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


statelist = []

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

desired_states = ["Alaska","Hawaii"]

directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/PollutionStates_Cenus_Block"
for filename in os.listdir(directory):
	if "EJScreen_Pollution" not in filename:
		continue 
	curr_state = getStateName(filename)
	statelist.append(curr_state)
	if (curr_state not in desired_states):
		continue

	numCensusTracts = 0
	prev_tract = ""
	rawEntriesToWrite_Dict = {} # These entries will have data lines from each census TRACT
	rawEntriesToWrite = [] # These entries will have data lines from each census TRACT
	incompleteTracts = []
	noPopulationTracts = []

	numLinesToOpen = -1
	iterNum = 0
	print "Reading File..."

	with open(directory + "/" + filename, 'rU') as f: 
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

	# Finish calculating each weighted scores, from the sums you had by dividing
	for key in rawEntriesToWrite_Dict:
		newEntry = rawEntriesToWrite_Dict[key]
		if (key not in incompleteTracts and isPopulated(newEntry,key)):
			for field in weightedFields:
				newEntry[fieldsWanted.index(field)] = newEntry[fieldsWanted.index(field)]/newEntry[fieldsWanted.index("pop")]
		else: 
			if (curr_state not in desired_states):
				for field in weightedFields:
					newEntry[fieldsWanted.index(field)] = "NA"
			else:
				for field in AK_HI_fields:
					if (isPopulated(newEntry,key)):
						newEntry[fieldsWanted.index(field)] = newEntry[fieldsWanted.index(field)]/newEntry[fieldsWanted.index("pop")]
				newEntry[fieldsWanted.index("o3")] = "NA"
				newEntry[fieldsWanted.index("pm")] = "NA"
		rawEntriesToWrite.append(newEntry)

	# Sort the entries
	rawEntriesToWrite_Sorted = sorted(rawEntriesToWrite[1:len(rawEntriesToWrite)], key=lambda entry: int(entry[1]))
	rawEntriesToWrite_Sorted.insert(0,rawEntriesToWrite[0])

	print "Writing " + curr_state + " Census Tract info to CSV File...."
	outFileName = "EJScreen_Pollution_FIPS_TRACTS_Sorted_" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(rawEntriesToWrite_Sorted)
	    f.close()
	print "Write complete! \n"


	nopestr1 = "Incomplete Pollution Data for the following tracts:"
	print nopestr1
	incompleteTracts.insert(0,nopestr1)
	for tract in incompleteTracts: print tract
	print "\n"


	nopestr2 = "No Population Data for the following tracts:"
	print nopestr2
	noPopulationTracts.insert(0,nopestr2)
	for tract in noPopulationTracts: print tract
	print "\n"
	outFileName = "Incomplete Pollution Data or No Population Tracts for " + curr_state + ".csv"
	with open(outFileName, "wb") as f:
		for line in incompleteTracts:
			f.write(line+ '\n')
		for line in noPopulationTracts:
			f.write(line+ '\n')
		f.close()


