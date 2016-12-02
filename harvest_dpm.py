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

def getStateName(filename):
	for statename in states:
		if (statename in filename and statename not in statelist):
			return statename



statelist = []
directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/Pollution TRACT Level Data"
for filename in os.listdir(directory):
	if "EJScreen" not in filename:
		continue 
		curr_state = getStateName(filename)
	# print filename
	# print curr_state
	statelist.append(curr_state)

	numLinesToOpen = 10
	iterNum = 0
	print "Reading File..."
	with open(directory + "/"+ "EJScreen_Pollution_FIPS_TRACTS_Sorted_" + curr_state + ".csv", 'rU') as f: 
	    reader = csv.reader(f)
	    fileHeader = []
	    numCensusTracts = 0;
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		add_pct_row(row, fileHeader,curr_state)
	    	else:
				fileHeader = row
	        iterNum +=1
	print "Fileread Complete! \n"
