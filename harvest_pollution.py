import csv
import numpy as np
import os
from scipy import stats



# Percentage:
# o3
# pm 
# traffic.score
# pctpre1960 ... pre1960/built_units


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

undesired_states = ["Alaska","Hawaii"]


def getTractFIPS(row,fileHeader):
	return row[fileHeader.index("FIPS")]

def getTractbuiltunits(row, fileHeader):
	return float(row[fileHeader.index("builtunits")])

def getTractpre1960(row, fileHeader):
	return float(row[fileHeader.index("pre1960")])

def getTracto3(row,fileHeader):
	return float(row[fileHeader.index("o3")])

def getTractpm(row,fileHeader):
	return float(row[fileHeader.index("pm")])

def getTracttraffic_score(row,fileHeader):
	if (row[fileHeader.index("traffic.score")] != "NA"):
		return float(row[fileHeader.index("traffic.score")])
	else:
		return -1

def pctpre1960(row, fileHeader):
	return (getTractpre1960(row, fileHeader)/getTractbuiltunits(row,fileHeader))

def add_pct_row(row, fileHeader):
	if (getTracttraffic_score(row,fileHeader) != -1 and getTractbuiltunits(row,fileHeader) != 0):
		newList = []
		o3_val = getTracto3(row, fileHeader)
		pm_val = getTractpm(row, fileHeader)
		traffic_val = getTracttraffic_score(row, fileHeader)
		pctpre1960_val = pctpre1960(row, fileHeader) 

		newList.append(pm_val) 
		newList.append(o3_val)
		newList.append(traffic_val) 
		newList.append(pctpre1960_val)

		percDict[getTractFIPS(row,fileHeader)] = newList
		o3_values.append(o3_val)
		pm_values.append(pm_val)
		traffic_values.append(traffic_val)
		pctpre1960_values.append(pctpre1960_val)
	else: 
		no_traffic_data_no_built_units.append(getTractFIPS(row,fileHeader))

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
	print filename
	print curr_state
	statelist.append(curr_state)
	if (curr_state in undesired_states):
		continue 

	numLinesToOpen = -1
	iterNum = 0
	percDict = {} # This variable can be seen in functions!
	o3_values = []
	pm_values = []
	traffic_values = []
	pctpre1960_values = []

	no_traffic_data_no_built_units = []
	print "Reading File..."
	with open(directory + "/"+ "EJScreen_Pollution_FIPS_TRACTS_Sorted_" + curr_state + ".csv", 'rU') as f: 
	    reader = csv.reader(f)
	    fileHeader = []
	    numCensusTracts = 0;
	    for row in reader:
	    	if (iterNum == numLinesToOpen):
	    		break
	    	if (iterNum != 0):
	    		add_pct_row(row, fileHeader)
	    	else:
				fileHeader = row
	        iterNum +=1
	print "Fileread Complete! \n"

	# Append percent_ist
	feature_list = [];
	feature_list.append(np.array(pm_values))
	feature_list.append(np.array(o3_values))
	feature_list.append(np.array(traffic_values))
	feature_list.append(np.array(pctpre1960_values))


	outfile_print = []
	perc_header = ["pm", "o3", "traffic", "pre1960"]
	outfile_header = ["FIPS", "pm", "pctpm", "o3", "pcto3", "traffic.score", "pct_traffic.score", "percpre1960", "pctpercpre1960"]
	for FIPS in percDict:
		curr_percentages = percDict[FIPS] 
		outfile_line = [FIPS]
		for feature in perc_header:
			ind = perc_header.index(feature)
			outfile_line.append(curr_percentages[ind])
			outfile_line.append(stats.percentileofscore(feature_list[ind], curr_percentages[ind], kind = "weak"))
		outfile_print.append(outfile_line)

	# Sort the entries
	outfile_print_Sorted = sorted(outfile_print[1:len(outfile_print)], key=lambda entry: int(entry[0]))
	outfile_print_Sorted.insert(0,outfile_header)


	print "Writing " + curr_state + " Percentiles for Pollution Data to CSV File..."
	outFileName = "CalEnviroScreen_tract_Pollution_Percentiles_" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(outfile_print_Sorted)
	    f.close()
	print "Write complete! \n"

	nopeStr =  "The following Census Tracts either had no built units or no traffic score: "
	no_traffic_data_no_built_units.insert(0,nopeStr)
	for tract in no_traffic_data_no_built_units:
		print tract
	outFileName = "Omitted Tracts for " + curr_state + ".csv"
	with open(outFileName, "wb") as f:
		for line in no_traffic_data_no_built_units:
			f.write(line+ '\n')
		f.close()
		print "Write complete! \n"	







