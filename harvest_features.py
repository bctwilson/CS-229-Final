import csv
import numpy as np
import os
from scipy import stats


# population density (pop/area), 
# min 
# lths 

# Percentage:
# pop/area, units of area, square-miles
# mins/pop, # minories
# lths/age25up, % of people over age 25 that have less than high school education


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


def getTractFIPS(row,fileHeader):
	return row[fileHeader.index("FIPS")]

def getTractPop(row, fileHeader):
	return float(row[fileHeader.index("pop")])

def getTractArea(row, fileHeader):
	return float(row[fileHeader.index("area")])

def getTractMins(row,fileHeader):
	return float(row[fileHeader.index("mins")])

def getTractLTHS(row,fileHeader):
	return float(row[fileHeader.index("lths")])

def getTract25(row,fileHeader):
	return float(row[fileHeader.index("age25up")])

def getTract5(row, fileHeader):
	return float(row[fileHeader.index("under5")])

def getTracthhlds(row, fileHeader):
	return float(row[fileHeader.index("hhlds")])

def getTractlingiso(row, fileHeader):
	return float(row[fileHeader.index("lingiso")])

def lingiso_pct(row, fileHeader):
	return 100*(getTractlingiso(row,fileHeader))/getTracthhlds(row,fileHeader)

def children_pct(row, fileHeader):
	return 100*(getTract5(row,fileHeader))/getTractPop(row,fileHeader)

def popden(row, fileHeader):
	return (getTractPop(row, fileHeader)/getTractArea(row,fileHeader))

def min_pct(row,fileHeader):
	return 100*(getTractMins(row,fileHeader)/getTractPop(row, fileHeader))

def lths_pct(row, fileHeader):
	return 100*(getTractLTHS(row, fileHeader)/getTract25(row,fileHeader))

def add_pct_row(row, fileHeader):
	if (getTractPop(row,fileHeader) != 0 and getTract25(row,fileHeader) != 0 and getTracthhlds(row,fileHeader) != 0):
		newList = []
		popden_Val = popden(row, fileHeader) 
		min_pctVal = min_pct(row, fileHeader)
		lths_pctVal = lths_pct(row, fileHeader)
		children_pctVal = children_pct(row, fileHeader)
		lingiso_pctVal = lingiso_pct(row, fileHeader)
		newList.append(popden_Val)
		newList.append(min_pctVal) 
		newList.append(lths_pctVal)
		newList.append(children_pctVal) 
		newList.append(lingiso_pctVal)
		percDict[getTractFIPS(row,fileHeader)] = newList
		popDens_values.append(popden_Val)
		mins_values.append(min_pctVal)
		lths_values.append(lths_pctVal)
		children_values.append(children_pctVal)
		lingiso_values.append(lingiso_pctVal)
	else: 
		no_pop_or_no_over_25.append(getTractFIPS(row,fileHeader))

def getStateName(filename):
	for statename in states:
		if (statename in filename and statename not in statelist):
			return statename

statelist = []
directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/SocioDemographic TRACT Level Data"
for filename in os.listdir(directory):
	if "EJScreen" not in filename:
		continue 
	curr_state = getStateName(filename)
	print filename
	print curr_state
	statelist.append(curr_state)

	numLinesToOpen = -1
	iterNum = 0
	percDict = {} # This variable can be seen in functions!
	popDens_values = []
	mins_values = []
	lths_values = []
	children_values = []
	lingiso_values = []
	no_pop_or_no_over_25 = []
	print "Reading File..."
	with open(directory + "/"+ "EJScreen_SocioDemographic_FIPS_TRACTS_Sorted_" + curr_state + ".csv", 'rU') as f: 
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
	feature_list.append(np.array(popDens_values))
	feature_list.append(np.array(mins_values))
	feature_list.append(np.array(lths_values))
	feature_list.append(np.array(children_values))
	feature_list.append(np.array(lingiso_values))


	outfile_print = []
	perc_header = ["popdense", "percmin", "perclths", "percchildren", "perclingiso"]
	outfile_header = ["FIPS", "popdense", "pctpopdense", "percmin", "pctmin", "perclths", "pctlths", "percchildren", "pctchildren", "perclingisohlds", "pctlingisohlds"]
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

	print "Writing " + curr_state + " Percentiles for Best Features to CSV File..."
	outFileName = "CalEnviroScreen_tract_Children_Lingisohhlds_FeaturePercentiles_" + curr_state + ".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(outfile_print_Sorted)
	    f.close()
	print "Write complete! \n"

	nopeStr =  "The following Census Tracts either had 0 population, 0 people over 25 years old, or 0 households: "
	no_pop_or_no_over_25.insert(0,nopeStr)
	for tract in no_pop_or_no_over_25:
		print tract
	outFileName = "Omitted Tracts for " + curr_state + ".csv"
	with open(outFileName, "wb") as f:
		for line in no_pop_or_no_over_25:
			f.write(line+ '\n')
		f.close()
		print "Write complete! \n"	








