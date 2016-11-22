import csv
import numpy 

import matplotlib; matplotlib.use('Agg') # Use a backend that doesn't require a display.
import matplotlib.pyplot as plt # Use the pyplot interface of matplotlib.
import pickle 


myEnviroObjects = [] # Intitalize empty set of huffmanObjects
enviroRows = []
global enviroHeader


fieldsWanted = [
	"Census Tract", 
	"CES 2.0 Score"
	]

def sanitizeRow(row, iterNum):
	newRow = filter(None, row)
	if (iterNum != 0):
		FIPS = row[0];
		FIPS = "0" + FIPS
		newRow[0] = FIPS
	return newRow


# Get index of each field, from the first row
def getFieldIndex(row, fieldIndex):
	shortHeader = [];
	for field in fieldsWanted:
		ind = row.index(field)
		fieldIndex.append(ind)
		shortHeader.append(row[ind])
	enviroRows.append(shortHeader)

def addEntry(row, fieldIndex):
	newEntry = []
	for ind in fieldIndex:
		newEntry.append(row[ind])
	enviroRows.append(newEntry)


numLinesToOpen = -1
iterNum = 0
print "Reading File..."

with open('CalEnviroScreen_formatted.csv', 'rU') as f: 
    reader = csv.reader(f)
    fieldIndex = []
    enviroHeader = [];
    numCensusTracts = 0;
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
    		addEntry(row,fieldIndex)
    	else:
    		enviroHeader = row
    		getFieldIndex(row, fieldIndex)
        iterNum +=1
print "Fileread Complete! \n"

# Sort the entries
enviroRowsSorted = sorted(enviroRows[1:len(enviroRows)-1], key=lambda entry: int(entry[0]))
enviroRowsSorted.insert(0,enviroRows[0])

print "Writing to CSV File...."
outFileName = "CalEnviroScreen_tract_scores.csv"
with open(outFileName, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(enviroRowsSorted)
    f.close()
print "Write complete! \n"


# # Pickle the songs

# pickle_filename = "California_SocioDemoGraphic_Lists.pkl"
# output = open(pickle_filename, 'wb')

# # Pickle California Data using protocol 0.
# pickle.dump(rawEntriesToWrite, output)