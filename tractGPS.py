import csv
import numpy as np
import os
from scipy import stats
import pandas as pd

states = ['Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


big_states_meanPLUS = ["70.96144","68.83175","66.86254", "76.64643", "71.56082", "74.73522",
	 "71.64926", "72.80835", "68.5743584601649", "74.60822", "67.67392", "73.69333", "69.37111", "69.61971", "72.63587"]

big_states = ["California", "Arizona", "Florida", "Georgia", "Illinois", "Michigan", "Indiana", "New York", "New Jersey",
	 "North Carolina", "Ohio", "Rhode Island", "Pennsylvania", "Texas", "Virginia"]

def getStateName(filename):
	for statename in states:
		if (statename in filename and statename not in statelist):
			return statename
	return "NOTHING"


def getTractFIPS_statefile(row, fileHeader):
	return row[fileHeader.index("CensusTract")]


def getBurdenScore(row, fileHeader):
	return row[fileHeader.index("BurdenScore")]

def convertFIPS(row, fileHeader):
	FIPS = row[fileHeader.index("CensusTract")]
	FIPS_quoted = "'" + FIPS + "'"
	row[fileHeader.index("CensusTract")] = FIPS_quoted

def addCoordinates(row, fileHeader, curr_state):
	currFIPS = getTractFIPS_statefile(row, fileHeader)
	if (currFIPS == ""):
		return
	currFIPS = int(currFIPS)
	if (currFIPS in FIPS_dict):
		curr_burden_score = getBurdenScore(row, fileHeader)			
		if (float(curr_burden_score) >= float(big_states_meanPLUS[big_states.index(curr_state)])):
			convertFIPS(row, fileHeader)
			new_entry = list(row)
			new_coords = FIPS_dict[currFIPS]
			new_entry[1]  = new_coords[0]
			new_entry[2] = new_coords[1]

			outfile_print.append(new_entry)
	else:
		missingFIPSs.append(currFIPS)



FIPS_dict = {}

print "Reading GPS Census Tract Datafile..."

df1 = pd.read_csv('tracts_GPS_national.csv', delim_whitespace=True)

for ind in range(len(df1)): 
	tractID = int(df1.iloc[ind,1])
	lat_coord = df1.iloc[ind,8] 
	long_coord = df1.iloc[ind,9]
	coordinates = [lat_coord,long_coord]
	FIPS_dict[tractID] = coordinates

print "Writing coordinates to state files..."

statelist = []

directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/Pollution Burden_Mapping"
for filename in os.listdir(directory): # Iterate through states... 
	if (getStateName(filename) == "NOTHING"):
		continue 
	curr_state = getStateName(filename)


	if (curr_state not in big_states):
		continue

	# print filename
	# print curr_state
	statelist.append(curr_state)
	fileHeader = []
	outfile_print = []

	missingFIPSs = []

	numLinesToOpen = -1
	iterNum = 0
	with open(directory + "/" + filename, 'rU') as f: 
	    reader = csv.reader(f)
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		addCoordinates(row, fileHeader, curr_state)
	    	else:
				fileHeader = row
				outfileHeader = list(row)
				outfile_print.append(outfileHeader)
	        iterNum +=1
	print "Fileread Complete! \n"

	print "Missing FIPS coordinates from " + curr_state +  " file:"
	print missingFIPSs

	print "Writing GPS Coordinates to Census Tract Mapping File for " + curr_state
	outFileName = "Predicted_Pollution_Score_CENSUS_TRACT_MAP_Coordinates_MEANPLUS1SD" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(outfile_print)
	    f.close()
	print "Write complete! \n"


	print "Writing Missing Census Tracts for " + curr_state
	missingFIPSs_filename = "Census_Tracts_Missing_Coordinates" + curr_state + ".csv"
	with open(missingFIPSs_filename, "wb") as f:
		for line in missingFIPSs:
			f.write(str(line)+ '\n')
		f.close()
	print "Write complete! \n"	