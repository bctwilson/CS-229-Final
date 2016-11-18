import csv

"""
Want to consider building a matrix of features and examples... 

Basic Examples: 

FIPS - Census FIPS code for block group
statename - Name of State
REGION = EPA Region Number
pm - PM2.5 level in air 
o3 - Ozone level in air 
pctmin - % Minority
pctlowinc = % Low Income
pctlths = % Lower than High School Education for Population 25 years and over
pctile.pm = %ile 2.5pm
pctile.o3 = %ile Ozone


"""
Entries = []
legend = []
fieldsWanted = ["FIPS", "statename", "REGION", "pm", "o3", "pctmin","pctlowinc","pctlths", "pctile.pm", "pctile.o3"]
fieldIndex = []

# Will eventually use a more efficient data-structure, like a matrix inside 
class Entry:
	"A class that contains desired data"
	def __init__(self, newRawData = []):

		rawData = newRawData 
		self.FIPS = rawData[fieldIndex[0]]
		self.state = rawData[fieldIndex[1]]
		self.REGION = rawData[fieldIndex[2]]
		self.pm = rawData[fieldIndex[3]]
		self.o3 = rawData[fieldIndex[4]]
		self.pctmin = rawData[fieldIndex[5]]
		self.pctlowinc = rawData[fieldIndex[6]]
		self.pctlths = rawData[fieldIndex[7]]
		self.pctilePM = rawData[fieldIndex[8]]
		self.pctileO3 = rawData[fieldIndex[9]]

# def 
# 36.02788332
# PCTL, EC in Excel
# Email: enviromail_group@epa.gov to ask about whether percentile is national or not 

# Processes the current line passed in
def addEntry(row, iterNum, file):
	newEntry = Entry(row)
	if (float(newEntry.pctlowinc) > .9 and newEntry.state == "California"):
		file.write("Current State: " + newEntry.state + '\n')
		file.write("Current FIPS: " + newEntry.FIPS + '\n') 
		file.write("Percent Low Income " + newEntry.pctlowinc + '\n') 
		file.write("Percentile PM 2.5: " + newEntry.pctilePM + '\n') 
		file.write("Percentile Ozone: "	+ newEntry.pctileO3 + '\n\n')
	Entries.append(newEntry)


# Get index of each field, from the first row
def getFieldIndex(row):
	ind = 0;
	for field in fieldsWanted:
		row.index(field)
		fieldIndex.append(row.index(field))
		ind += 1;
	print fieldIndex

# Put each line of the file into a python list. 

file = open("California_90_Percent.txt", "w")
dataLines = []
print 'Loading EJCSREEN file...\n'
numLinesToOpen = -1
iterNum = 0
print "Reading File..."
with open('EJSCREEN_20150505.csv', 'rU') as f: 
    reader = csv.reader(f)
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
        	addEntry(row, iterNum, file)     
    	else:
    		getFieldIndex(row)
        iterNum +=1
file.close()
print "Complete!"

