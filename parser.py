import csv
import numpy 

import matplotlib; matplotlib.use('Agg') # Use a backend that doesn't require a display.
import matplotlib.pyplot as plt # Use the pyplot interface of matplotlib.
import pickle 

def create_graph(title, output, graphs):
    """Helper function for creating a graph."""
    colors = [('red', 'blue'), ('green', 'yellow')]

    plt.figure(figsize=(8, 8))
    plt.title(title)

    for i, (filename, ack_label, data_label) in enumerate(graphs):
        acks, data = load_pcap(filename)
        plt.scatter(map(itemgetter(0), acks), map(itemgetter(1), acks), c=colors[i][0], marker='x', label=ack_label)
        plt.scatter(map(itemgetter(0), data), map(itemgetter(1), data), c=colors[i][1], label=data_label)
    
    plt.xlabel("Time (sec)")
    plt.ylabel("Sequence Number (bytes)")
    plt.legend(loc='lower right', fontsize=10)
    
    plt.savefig(output)


"""

Census Track Format: 
https://www.cubitplanning.com/data/census-tract-numbers

https://en.wikipedia.org/wiki/Census_block
https://en.wikipedia.org/wiki/Census_block_group

https://transition.fcc.gov/form477/Geo/more_about_census_tracts.pdf

06067001101 1

FORMAT:

06|067|001101

Example, OBJECT ID 19996: 

06|067|001101|1 [California, Sacremento County, Tract 11.01, Block Group (single digit)], overall 12-digit number, 11 digit census tract

"""
Entries = []
legend = []
# fieldsWanted = ["FIPS", "statename", "REGION", "pm", "o3", "pctmin","pctlowinc","pctlths", "pctile.pm", 
# 	"pctile.o3"] 
fieldsWanted = [
	"OBJECTID", 
	"FIPS", 
	"ST",  
	"statename", 
	"REGION", 
	"area", 
	"pop", 

	"lowinc", 
	"pctlowinc", 
	"pctile.pctlowinc", 
	"povknownratio", 

	"mins", 
	"pctmin", 
	"pctile.pctmin", 


	"under5", 
	"pctunder5", 
	"pctile.pctunder5", 

	"over64", 
	"pctover64", 
	"pctile.pctover64", 

	"age25up", 
	"lths", 
	"pctlths", 
	"pctile.pctlths", 

	"hhlds", 
	"lingiso", 
	"pctlingiso", 
	"pctile.pctlingiso", 

	"builtunits", 
	"pre1960", 
	"pctpre1960", 
	"pctile.pctpre1960", 

	"traffic.score", 
	"pctile.traffic.score", 
]


rawEntriesToWrite = []; # A list of the raw CSV rows, with the desired data to write


# Will eventually use a more efficient data-structure, like a matrix inside 
class Entry:
	"A class that contains desired data"
	def __init__(self, newRawData = []):

		rawData = newRawData 
		self.FIPS = rawData[fieldIndex[fieldsWanted.index("FIPS")]]
		self.state = rawData[fieldIndex[fieldsWanted.index("statename")]]
		# self.REGION = rawData[fieldIndex[fieldsWanted.index("REGION")]]
		# self.pm = rawData[fieldIndex[fieldsWanted.index("pm")]]
		# self.o3 = rawData[fieldIndex[fieldsWanted.index("o3")]]
		# self.pctmin = rawData[fieldIndex[fieldsWanted.index("pctmin")]]
		# self.pctlowinc = rawData[fieldIndex[fieldsWanted.index("pctlowinc")]]
		# self.pctlths = rawData[fieldIndex[fieldsWanted.index("pctlths")]]
		# self.pctilePM = rawData[fieldIndex[fieldsWanted.index("pctilePM")]]
		# self.pctileO3 = rawData[fieldIndex[fieldsWanted.index("pctileO3")]]

# def 
# 36.02788332
# PCTL, EC in Excel
# Email: enviromail_group@epa.gov to ask about whether percentile is national or not 



# Processes the current line passed in
def addEntry(row, fieldIndex, iterNum = -1, file = "",):
	newEntry = Entry(row)
	if (newEntry.state == "California"):
		newRawEntry = [];
		for index in fieldIndex: # Write desired data into a python list. 
			newRawEntry.append(row[index]) 
		rawEntriesToWrite.append(newRawEntry)
		Entries.append(newRawEntry)


# Get index of each field, from the first row
def getFieldIndex(row, fieldIndex):
	shortHeader = [];
	for field in fieldsWanted:
		ind = row.index(field)
		fieldIndex.append(ind)
		shortHeader.append(row[ind])
	rawEntriesToWrite.append(shortHeader)



# BEGIN PROGRAM ->>>>>>>->>>>>>>->>>>>>>->>>>>>>->>>>>>>->>>>>>>->>>>>>>->>>>>>>

# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()

# Put each line of the file into a python list. 

#file = open("California_90_Percent_2.txt", "w") # File to
dataLines = []
print 'Loading EJCSREEN file...\n'
numLinesToOpen = -1
iterNum = 0
print "Reading File..."
with open('EJSCREEN_20150505.csv', 'rU') as f: 
    reader = csv.reader(f)
    fieldIndex = []
    numCensusTracts = 0;
    for row in reader:
    	if (iterNum == numLinesToOpen):
    		break
    	if (iterNum != 0):
        	addEntry(row, fieldIndex)     
    	else:
    		getFieldIndex(row, fieldIndex)
        iterNum +=1
print "Fileread Complete! \n"

# print "Writing to CSV File...."
# outFileName = "EJScreen_SocioDemographic_California2.csv"
# with open(outFileName, "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(rawEntriesToWrite)
# print "Write complete!"

# Pickle the songs

pickle_filename = "California_SocioDemoGraphic_Lists.pkl"
output = open(pickle_filename, 'wb')

# Pickle California Data using protocol 0.
pickle.dump(rawEntriesToWrite, output)

output.close()
