import csv
import numpy as np
import os
from scipy import stats


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

states_abrv = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
	'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
	'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def getStateName(filename):
	for statename in states:
		if (statename in filename and statename not in statelist):
			return statename

def getStateAbbrv(row, fileHeader):
	return row[fileHeader.index("State")]

def getTractFIPS(row, fileHeader):
	return row[fileHeader.index("Tract")]	

def getTractFIPS_statefile(row, fileHeader):
	return row[fileHeader.index("FIPS")]

def getTractConc(row, fileHeader):
	return float(row[fileHeader.index("Total Conc")])	

def addDpmEntry(row, fileHeader):
	state_abbrv = getStateAbbrv(row,fileHeader)
	if (state_abbrv in dpmDict):
		FIPS_dict = dpmDict[state_abbrv] # this is another dictionary
		FIPS_dict[getTractFIPS(row,fileHeader)] = getTractConc(row,fileHeader) # Add FIPS, Total Conc Pair
		dpmDict[state_abbrv] = FIPS_dict # Update value in dpmDict
	else:
		new_FIPS_dict = {}
		new_FIPS_dict[getTractFIPS(row, fileHeader)] = getTractConc(row, fileHeader)
		dpmDict[state_abbrv] = new_FIPS_dict # Create a new dictionary with first entry

def state_to_abbrv(curr_state):
	return states_abrv[states.index(curr_state)]

def add_DPM_Value1(row, fileHeader, curr_state):
	wanted_FIPS = getTractFIPS_statefile(row, fileHeader)
	# print fileHeader
	# print "Wanted FIPS for this ROW: "
	# print wanted_FIPS
	st_abrv =  state_to_abbrv(curr_state)
	# print st_abrv
	state_dpms = dpmDict[st_abrv]  # Dictionary of FIPS and dpm value pairs for current state
	if (wanted_FIPS in state_dpms):
		dpm_values.append(state_dpms[wanted_FIPS])
	
	# We just want to return the value to be converted to percentile... 
def findDPM_state(row, fileHeader, curr_state): 
	wanted_FIPS = getTractFIPS_statefile(row, fileHeader)
	st_abrv =  state_to_abbrv(curr_state)
	state_dpms = dpmDict[st_abrv]  # Dictionary of FIPS and dpm value pairs for current state
	if (wanted_FIPS in state_dpms):
		return state_dpms[wanted_FIPS]

# INSTRUCTIONS: 

# 1. Make a dictionary, where the key is the state abbreviation. The value will be another dictionary: {FIPS_KEY, Total Conc_VALUE} 
# 2. Go through each FIPS in the statefile you're in, and search for the FIPS, and return the CONC_Value, make sure it's not N/A so you can percentile 
#  	the usable Data. Add to OUTFILE_DIC {FIPS, row} and Add to dpm_values 
#  3. Iterate through OUTFILE_DIC, get last element, calculate percentile from dpm_values. Append dat to the row of "outfile_print" variables (list of lists...)
#  4. Write that to a file 


numLinesToOpen = -1
iterNum = 0
dpmDict = {}
with open("DIESEL_PM_Shrunked.csv", 'rU') as f: 
    reader = csv.reader(f)
    fileHeader = []
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
    		addDpmEntry(row, fileHeader)
    	else:
			fileHeader = row
        iterNum +=1
print "Fileread Complete! \n"

print "DIESEL PM DICTIONARY COMPLETE..."
dpm_fileheader = fileHeader
for key in dpmDict:
	print key
# print dpmDict

statelist = []
directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/Pollution TRACT Percentile Data, ALL STATES, EJSCREEN SET, NO DPM"
for filename in os.listdir(directory): # Iterate through states... 
	if ("CalEnviroScreen" not in filename or "Omitted" in filename):
		continue 
	curr_state = getStateName(filename)
	# print filename
	# print curr_state
	statelist.append(curr_state)

	# if (curr_state != "Alaska"):
	# 	continue

	numLinesToOpen = -1
	iterNum = 0
	dpm_values = []

	# Do one pass getting all the DPM values for census tracts we care about. 
	print "Reading File pass 1 of 2 to get DPM values for percentile calculation..."
	with open(directory + "/"+ "CalEnviroScreen_tract_ALL_POLLUTION_Percentiles_" + curr_state + ".csv", 'rU') as f: 
	    reader = csv.reader(f)
	    fileHeader = []
	    numCensusTracts = 0;
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		add_DPM_Value1(row,fileHeader,curr_state) # Find CONC value,  add to dpm_values
	    	else:
				fileHeader = row
	        iterNum +=1
	f.close()
	print "Fileread Complete! \n"

	# print dpm_values
	# print "\n\n\n"

	outfile_print = []

	iterNum = 0
	print "Reading File pass 2 of 2 to get DPM values for percentile calculation..."
	with open(directory + "/"+ "CalEnviroScreen_tract_ALL_POLLUTION_Percentiles_" + curr_state + ".csv", 'rU') as f: 
	    reader = csv.reader(f)
	    fileHeader = []
	    numCensusTracts = 0;
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		updated_row = row
	    		updated_row.append(findDPM_state(row, fileHeader, curr_state))
	    		updated_row.append(stats.percentileofscore(dpm_values, findDPM_state(row, fileHeader, curr_state), kind = "weak"))
	    		outfile_print.append(updated_row)
	    	else:
				fileHeader = row
	        iterNum +=1
	f.close()
	print "Fileread Complete! \n"

	if (curr_state != "Hawaii" and curr_state != "Alaska"):

		outfile_header = fileHeader
		outfile_header.append("dpm_total_conc")
		outfile_header.append("pct_dpm")
		outfile_print.insert(0,outfile_header)
	else:
		outfile_header = fileHeader
		outfile_header[len(outfile_header)-2] = "dpm_total_conc"
		outfile_header[len(outfile_header)-1] = "pct_dpm"
		outfile_header.append("o3") 
		outfile_header.append("pcto3")
		outfile_print.insert(0,outfile_header)



	# print outfile_print

	print "Adding DPM Percentile data for " + curr_state + " to Percentiles Pollution Data CSV File..."
	outFileName = "CalEnviroScreen_tract_ALL_POLLUTION_WITH_DPM_Percentiles_" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(outfile_print)
	    f.close()
	print "Write complete! \n"

