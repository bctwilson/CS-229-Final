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

# 1) PM2.5, YES
# 2) O3, YES
# 3) Diesel PM, SEE OTHER FILE
# 4) Proximity to Risk Management Plan (RMP) sites, GETTING
# 5) Traffic proximity and volume, YES, Traffic Score YES
# 6) Proximity to National Priorities List (NPL) sites, GETTING
# 7) Proximity to major direct water dischargers (NPDS), GETTING
# 8) Proximity to Treatment Storage and Disposal Facilities (TSDFs), GETTING


def getTractFIPS(row,fileHeader):
	return row[fileHeader.index("FIPS")]

def getTractbuiltunits(row, fileHeader):
	return float(row[fileHeader.index("builtunits")])

def getTractpre1960(row, fileHeader):
	return float(row[fileHeader.index("pre1960")])

def getTracto3(row,fileHeader, curr_state): 
	if (curr_state not in undesired_states):
		return float(row[fileHeader.index("o3")])
	else:
		return "N/A"

def getTractpm(row,fileHeader, curr_state):
	if (curr_state not in undesired_states):
		return float(row[fileHeader.index("pm")])
	else:
		return "N/A"

def getTracttraffic_score(row,fileHeader):
	if (row[fileHeader.index("traffic.score")] != "NA"):
		return float(row[fileHeader.index("traffic.score")])
	else:
		return -1

def getTractnpdes(row,fileHeader):
	return float(row[fileHeader.index("proximity.npdes")])

def getTractnpl(row,fileHeader):
	return float(row[fileHeader.index("proximity.npl")])

def getTractrmp(row,fileHeader):
	return float(row[fileHeader.index("proximity.rmp")])

def getTracttsdf(row,fileHeader):
	return float(row[fileHeader.index("proximity.tsdf")])

def pctpre1960(row, fileHeader):
	return 100*(getTractpre1960(row, fileHeader)/getTractbuiltunits(row,fileHeader))

def proximityOkay(row, fileHeader):
	prox_vals = [];
	prox_vals.append(getTractnpdes)
	prox_vals.append(getTractnpl)
	prox_vals.append(getTractrmp)
	prox_vals.append(getTracttsdf)
	return ("NA" not in prox_vals)

def add_pct_row(row, fileHeader, curr_state):
	if (getTracttraffic_score(row,fileHeader) != -1 and getTractbuiltunits(row,fileHeader) != 0 and proximityOkay(row,fileHeader)):
		newList = []
		o3_val = getTracto3(row, fileHeader, curr_state)
		pm_val = getTractpm(row, fileHeader, curr_state)
		traffic_val = getTracttraffic_score(row, fileHeader)
		pctpre1960_val = pctpre1960(row, fileHeader) 

		npdes_val = getTractnpdes(row, fileHeader)
		npl_val = getTractnpl(row, fileHeader)
		rmp_val = getTractrmp(row, fileHeader)
		tsdf_val = getTracttsdf(row, fileHeader)

		newList.append(traffic_val) 
		newList.append(pctpre1960_val)
		newList.append(npdes_val)
		newList.append(npl_val)
		newList.append(rmp_val)
		newList.append(tsdf_val)
		newList.append(pm_val) 
		newList.append(o3_val)



		percDict[getTractFIPS(row,fileHeader)] = newList
		traffic_values.append(traffic_val)
		pctpre1960_values.append(pctpre1960_val)

		npdes_values.append(npdes_val)
		npl_values.append(npl_val)
		rmp_values.append(rmp_val)
		tsdf_values.append(tsdf_val)
		pm_values.append(pm_val)
		o3_values.append(o3_val)
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
	# print filename
	# print curr_state
	statelist.append(curr_state)

	numLinesToOpen = -1
	iterNum = 0
	percDict = {} # This variable can be seen in functions!
	o3_values = []
	pm_values = []
	traffic_values = []
	pctpre1960_values = []

	npdes_values = []
	npl_values = []
	rmp_values = []
	tsdf_values = []

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
	    		add_pct_row(row, fileHeader,curr_state)
	    	else:
				fileHeader = row
	        iterNum +=1
	print "Fileread Complete! \n"

	# Append percent_ist
	feature_list = [];
	feature_list.append(np.array(traffic_values))
	feature_list.append(np.array(pctpre1960_values))

	# New thangs
	feature_list.append(np.array(npdes_values))
	feature_list.append(np.array(npl_values))
	feature_list.append(np.array(rmp_values))
	feature_list.append(np.array(tsdf_values))

	# Reordering
	feature_list.append(np.array(pm_values))
	feature_list.append(np.array(o3_values))


	outfile_print = []
	perc_header = ["traffic", "pre1960", "npdes", "npl", "rmp", "tsdf", "pm", "o3"]
	outfile_header = ["FIPS", "traffic.score", "pct_traffic.score", "percpre1960", "pctpercpre1960",
		"percproximity.npdes", "pctproximity.npdes", "percproximity.npl", "pctproximity.npl", "percproximity.rmp", "pctproximity.rmp", "percproximity.tsdf","pctproximity.tsdf", "pm", "pctpm", "o3", "pcto3"]
	for FIPS in percDict:
		curr_percentages = percDict[FIPS] 
		outfile_line = [FIPS]
		for feature in perc_header:
			ind = perc_header.index(feature)
			outfile_line.append(curr_percentages[ind])
			if ( (curr_state == "Alaska" or curr_state == "Hawaii") and (perc_header[ind] == "pm" or perc_header[ind] == "o3" ) ): # Don't add that to line
				pass
			else:
				outfile_line.append(stats.percentileofscore(feature_list[ind], curr_percentages[ind], kind = "weak"))
		outfile_print.append(outfile_line)

	# Sort the entries
	outfile_print_Sorted = sorted(outfile_print[1:len(outfile_print)], key=lambda entry: int(entry[0]))
	outfile_print_Sorted.insert(0,outfile_header)


	print "Writing " + curr_state + " Percentiles for Pollution Data to CSV File..."
	outFileName = "CalEnviroScreen_tract_ALL_POLLUTION_Percentiles_" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(outfile_print_Sorted)
	    f.close()
	print "Write complete! \n"

	nopeStr =  "The following Census Tracts either had no built units, no traffic score, or incomplete proximity data: "
	no_traffic_data_no_built_units.insert(0,nopeStr)
	for tract in no_traffic_data_no_built_units:
		print tract
	outFileName = "Omitted Tracts for " + curr_state + ".csv"
	with open(outFileName, "wb") as f:
		for line in no_traffic_data_no_built_units:
			f.write(line+ '\n')
		f.close()
		print "Write complete! \n"	







