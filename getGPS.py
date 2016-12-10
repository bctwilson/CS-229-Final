import csv
import numpy as np
import os
from scipy import stats


states = ['Alabama', 'Arizona', 'Arkansas', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

def getState(row,fileHeader):
	return row[fileHeader.index("State")]

def getZIP_GPSFile(row, fileHeader):
	return row[fileHeader.index("zip")]

def getZIP(row, fileHeader):
	return row[fileHeader.index("ZIP")]

def getLat(row, fileHeader):
	return row[fileHeader.index("latitude")]

def getLong(row, fileHeader):
	return row[fileHeader.index("longitude")]	

def getBurdenScore(row, fileHeader):
	return row[fileHeader.index("burdenscore")] 	

def convertFIPS(row, fileHeader):
	FIPS = row[fileHeader.index("FIPS")]
	FIPS_quoted = "'" + FIPS + "'"
	row[fileHeader.index("FIPS")] = FIPS_quoted

def getCoordinates(row, fileHeader):
	new_list = []
	new_list.append(getLat(row,fileHeader))
	new_list.append(getLong(row,fileHeader))
	return new_list


def updateDict(row, fileHeader):
	curr_ZIPValue = getZIP_GPSFile(row, fileHeader)
	GPS_dict[curr_ZIPValue] = getCoordinates(row, fileHeader)

def addCoordinates(row, fileHeader, curr_state):
	if (getState(row,fileHeader) == curr_state):
		currZip = getZIP(row, fileHeader)
		if (currZip in GPS_dict):
			curr_burden_score = getBurdenScore(row, fileHeader)			
			if (float(curr_burden_score) >= 80):
				convertFIPS(row, fileHeader)
				new_entry = list(row+GPS_dict[currZip])
				outfile_print.append(new_entry)
		else:
			missingZIPs.append(currZip)


# INSTRUCTIONS: 

# 1. Go through each state file, and make a dictionary of the pollution tract scores. Key: CENSUS TRACT (a string, leading zeros are gone...)
# 2. Do not include any tracts from Alaska or Hawaii in the dictionary. 
# 3.

# 1. AFter DICTIONARY WITH EJSCREEN SHIT. Iterate through ZIPCODE, make entry like ABQ one, using known information from previous.. 

# state_dictionary  {FIPS, [value,value,value]}

# 1. Get a dictionary  of latitudes and longitudes, and convert ZIP to double... at ALL TIMES. {FIPS_DOUBLE, [latitude, longitude] }

GPS_dict = {}

numLinesToOpen = -1
fileHeader = []

iterNum = 0
print "Reading ZIPCODE File for GPS Coordinates..." 
with open("zip_code_database.csv", 'rU') as f: 
    reader = csv.reader(f)
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
    		updateDict(row, fileHeader)	    		
    	else:
    		fileHeader = row
        iterNum +=1
f.close()
print "Fileread Complete! \n"

# for key in GPS_dict:
# 	print key
# 	print GPS_dict[key]


for curr_state in states:
	fileHeader = []
	outfile_print = []

	missingZIPs = []

	numLinesToOpen = -1
	iterNum = 0
	with open("NATIONAL_Predicted_Pollution_Score_MAP_with_State.csv", 'rU') as f: 
	    reader = csv.reader(f)
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		addCoordinates(row, fileHeader, curr_state)
	    	else:
				fileHeader = row
				outfileHeader = list(row)
				outfileHeader.append("latitude")
				outfileHeader.append("longitude")
				outfile_print.append(outfileHeader)
	        iterNum +=1
	print "Fileread Complete! \n"

	print "Missing ZIP Code coordinates from file: "
	print missingZIPs

	print "Writing GPS Coordinates to ZIP-Code, Census Tract Mapping File for " + curr_state
	outFileName = "Predicted_Pollution_Score_MAP_Coordinates_over_80" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(outfile_print)
	    f.close()
	print "Write complete! \n"


