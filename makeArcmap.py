import csv
import numpy as np
import os
from scipy import stats


states = ['Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


def getStateName(filename):
	for statename in states:
		if (statename in filename and statename not in statelist):
			return statename
	return "NOTHING"

def getBurdenScore(row, fileHeader):
	return row[fileHeader.index("burdenscore")]

def getTractFIPS(row, fileHeader):
	return row[fileHeader.index("TRACT")]	# For ZIP CODE FILE

def getTractFIPS_statefile(row, fileHeader):
	return row[fileHeader.index("FIPS")]

def getZIP(row, fileHeader):
	return row[fileHeader.index("ZIP")]

def updateDict(row, fileHeader, curr_state):
	row.append(curr_state)
	FIPS_dict[int(getTractFIPS_statefile(row, fileHeader))] = row

def addZIPEntry(row, fileHeader):
	curr_FIPS = int(getTractFIPS(row, fileHeader))
	if (curr_FIPS in FIPS_dict):
		next_entry = list(FIPS_dict[curr_FIPS])
		ZIP_String = str(getZIP(row, fileHeader))
		next_entry.append(ZIP_String)
		outfile_print.append(next_entry)

# INSTRUCTIONS: 

# 1. Go through each state file, and make a dictionary of the pollution tract scores. Key: CENSUS TRACT (a string, leading zeros are gone...)
# 2. Do not include any tracts from Alaska or Hawaii in the dictionary. 
# 3.

# 1. AFter DICTIONARY WITH EJSCREEN SHIT. Iterate through ZIPCODE, make entry like ABQ one, using known information from previous.. 

# state_dictionary  {FIPS, [value,value,value]}

FIPS_dict = {}
statelist = []
directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/Pollution Burden Scores"
for filename in os.listdir(directory): # Iterate through states... 
	if (getStateName(filename) == "NOTHING"):
		continue 
	curr_state = getStateName(filename)
	# print filename
	# print curr_state
	statelist.append(curr_state)


	numLinesToOpen = -1
	fileHeader = []

	iterNum = 0
	print "Reading Pollution Score File for ..." + curr_state
	with open(directory + "/"+ curr_state + ".csv", 'rU') as f: 
	    reader = csv.reader(f)
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		updateDict(row, fileHeader, curr_state)	    		
	    	else:
	    		fileHeader = row
	        iterNum +=1
	f.close()
	print "Fileread Complete! \n"

# for key in FIPS_dict:
# 	print FIPS_dict[key]


# Part 2.. 

outfileHeader = fileHeader # Save all the header info from the previous file... 
outfileHeader.append("State")
outfileHeader.append("ZIP")
fileHeader = []
outfile_print = []
outfile_print.append(outfileHeader)

numLinesToOpen = -1
iterNum = 0
with open("ZIP_TRACT_062015_CLEAN.csv", 'rU') as f: 
    reader = csv.reader(f)
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
    		addZIPEntry(row, fileHeader)
    	else:
			fileHeader = row
        iterNum +=1
print "Fileread Complete! \n"

print "Writing Mapping File, with all ZIPCODES, and corresponding FIPS Census Tracts"
outFileName = "NATIONAL_Predicted_Pollution_Score_MAP_with_State_ALABAMA35004.csv"
with open(outFileName, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(outfile_print)
    f.close()
print "Write complete! \n"


