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

CALENVIROSCREEN: 06|019|000902

"""

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
	'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 
	'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
	'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
	'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


fieldsWanted = [
	"OBJECTID", 
	"FIPS", 
	"ST",  
	"statename", 
	"REGION", 
	"area", 
	"pop", 

	"builtunits", 
	"pre1960", 
	"o3", 
	"pm", 
	"proximity.npdes", 
	"proximity.npl", 
	"proximity.rmp", 
	"proximity.tsdf", 
	"traffic.score", 

]


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



# Processes the current line passed in
def addEntry(row, fieldIndex, curr_state, iterNum = -1, file = "",):
	newEntry = Entry(row)
	if (newEntry.state == curr_state):
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

for curr_state in states:

	rawEntriesToWrite = []; # A list of the raw CSV rows, with the desired data to write
	Entries = []
	legend = []

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
	        	addEntry(row, fieldIndex, curr_state)     
	    	else:
	    		getFieldIndex(row, fieldIndex)
	        iterNum +=1
	print "Fileread Complete! \n"

	# Sort the entries. OUTPUT SORTED DATA
	rawEntriesToWrite_Sorted = sorted(rawEntriesToWrite[1:len(rawEntriesToWrite)], key=lambda entry: int(entry[1]))
	rawEntriesToWrite_Sorted.insert(0,rawEntriesToWrite[0])

	print "Writing " + curr_state + " SocioDemographic data to CSV File...."
	outFileName = "EJScreen_Pollution_" + curr_state +".csv"
	with open(outFileName, "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(rawEntriesToWrite_Sorted)
	print "Write complete!"



