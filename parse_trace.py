from collections import Counter

class Entry:
	"A class that contains the raw lines of an IP or ARP Entry"
	def __init__(self, newType = "", firstLine = ""):

		self.numLines = 1 # number of lines
		self.lines = [firstLine] # raw lines of text
		self.type = newType # type of entry, IP or ARP

	def addLine(self,newline):
		if (newline != "" and newline != "\n"):
			self.lines.append(newline)
			self.numLines += 1

	# IP
	# IP (tos 0x0, ttl 128, id 3053, offset 0, flags [none], proto UDP (17), length 142)
    # 10.30.14.99.17500 > 255.255.255.255.17500: UDP, length 114

# Takes in an input of the first line, as a list of space-delimited strings and returns the type (ARP or IP)
def isBeginEntry(currLine):
	splitLine = currLine.split() # split the line up
	if (len(splitLine) == 0): return ""
	if (splitLine[0] == "IP" or splitLine[0] == "ARP,"):
		return splitLine[0].replace(",","") # remove the commma
	else:
		return ""

def findEndOfEntry(Entries,dataLines,currLineNum):
	i = currLineNum 
	while True:
		# check if we are at the end of the data
		if (i > len(dataLines) -1): 
			return i 
		currLine = dataLines[i] # get current line of data
		if (isBeginEntry(currLine) != ""): # "IP or "ARP" was found at the beginning of this line
			return i
		Entries[len(Entries)-1].addLine(currLine) # append the current line to the most recently added entry
		i +=1

# Takes in the data, the list of entries, and the current line number, which should be on the line for the next entry or end of file. 
def findNextEntry(currLineNum, dataLines, Entries):
	while True:
		if (currLineNum > (len(dataLines) - 1)): # Checks if the current line number is within the database
			return -1;
		currLine = dataLines[currLineNum] # Get current line
		first_token = isBeginEntry(currLine) # first token of the line
		if (first_token != ""): # first token MUST be an IP or ARP
			Entries.append(Entry(first_token,currLine))
			return_value =  findEndOfEntry(Entries,dataLines,currLineNum+1) # Will update currLine to be at the beginning of the next entry 
			return return_value

# Return destination IP from an IP entry, which is in the second line
def getDestIP(secondLine):
	split_line = secondLine.split()
	return split_line[2].replace(":","")

# Return destination IP from an IP entry, which is in the second line
def getSourceIP(secondLine):
	split_line = secondLine.split()
	return split_line[0]

# Removes port number from IP address
def removePortNumber(IP_addr):
	splitIP = IP_addr.split(".")
	return (splitIP[0] + "." + splitIP[1] + "." + splitIP[2] + "." + splitIP[3])

# Extracts port number from IP address
def getPortNumber(IP_addr):
	splitIP = IP_addr.split(".")
	return splitIP[4]

# Extracts protocol from first line of IP entry
def whatProtocol(firstLine):
	split_line = firstLine.split()
	proto_location = split_line.index("proto") + 1
	return split_line[proto_location]

# Get the sequence number of the packet, e.g. desired_number:ack_value_expected_in_response (seqno + length + 1)
def getseqno(secondLine):
	split_line = secondLine.split()
	seq_pair_location = split_line.index("seq") + 1
	seq_pair = split_line[seq_pair_location] # Gets num:num value from the line
	numbers_only = seq_pair.split(":") # Removes the colon between both numbers, the second number is left with a common though
	return int(numbers_only[0])

"""
First, search for any lines that have 10.30.22.101 as the source address. And the destination address has port 80. "

i) First, find any line that has IP, take each line until you see a line that starts with IP or ARP

Example:
IP (tos 0x0, ttl 64, id 31771, offset 0, flags [DF], proto TCP (6), length 52)
    10.30.22.101.64122 > 74.125.239.120.443: Flags [.], cksum 0xe51b (correct), ack 31585, win 4039, options [nop,nop,TS val 408458751 ecr 4243103487], length 0
"""


# Put each line of the file into a python list. 
dataLines = []
print 'Loading file...\n'
with open('trace.txt') as tracefile:
    for line in tracefile:
        dataLines.append(line) 

# Group each line into a set of Entries that will either be ARP or IP. Each Entry will only have the type and the raw lines
Entries = []
currLineNum = 0


while True:
	if (currLineNum == -1):
		break
	currLineNum = findNextEntry(currLineNum, dataLines, Entries)

# # Debugging
# print "Print all found entries: "
# for entry in Entries:
# 	print entry.type
# 	print entry.numLines
# 	print entry.lines

# PART I: Search for what websites mobile device accesses and list them. 
print "PART I: Looking for websites that the mobile device accessed; websites typically listen on port 80 ... \n\n"
mobile_IP = "10.30.22.101"
index = 1
acceessed_IPs = []

for entry in Entries:
	if (entry.type == "IP" and whatProtocol(entry.lines[0]) == "TCP"): # Checks for TCP protocol 
		secondLine = entry.lines[1] 
		if ( (mobile_IP in secondLine) and (".80:" in secondLine) and ("[S]" in secondLine) ): # the colon after .80 means that it was accessed, and make sure it's a SYN, just to be safe
			new_IP = getDestIP(secondLine) # Get destination IP
			if (acceessed_IPs.count(new_IP) == 0):
				acceessed_IPs.append(new_IP) # Add new IP address to the list
				print "At entry #%d) "%index + secondLine # Print that line
				# print "Accessed IP Address without Port: " + removePortNumber(new_IP)  
	index += 1


# PART II and III: 
print "PARTS II AND III: Looking for hosts performing port scanning and port flooding...\n\n"

# Look for all IP Address that are performing SYN requests and the count of SYN requests made.
pair_count = Counter() # Maintains a count of number of SYN requests from a source to destination IP address
port_numbers_flood = []
port_numbers_scanned = []

# Known values based on output of part II and III script
portflood_attacker = "10.30.12.152"
portflood_victim = "10.30.17.255"

# Print out port number after you find culprit... 
portscanned_attacker = "10.30.1.65"
portscanned_victim = "10.30.5.234"

for entry in Entries: 
	if (entry.type == "IP" and whatProtocol(entry.lines[0]) == "TCP" ): # Checks for TCP protocol
		secondLine = entry.lines[1]
		if ( "[S]" in secondLine):  # Check for SYNs
			sourceIP = getSourceIP(secondLine)
			destIP = getDestIP(secondLine)
			pair_count[ ( removePortNumber(sourceIP), removePortNumber(destIP) ) ] += 1 # Add the count of IP pairs to the list

			# Add port number to the list of scanned port numbers
			if (removePortNumber(sourceIP) == portscanned_attacker and removePortNumber(destIP) == portscanned_victim):  
				port_numbers_scanned.append(getPortNumber(destIP)) 

			# Add port number to the list of flooded port numbers
			if (removePortNumber(sourceIP) == portflood_attacker and removePortNumber(destIP) == portflood_victim):  
				port_numbers_flood.append(getPortNumber(destIP)) 


print "Most common source-dest SYN pairs: " # IP Address: 10.30.12.152, tried to access 10.30.17.255 a total of 26076 times!!!! 
print pair_count.most_common(3)

print "*Notice that the first most common pair is the port scanning attack, and the second most common pair is the syn-flooding attack.\n"

port_numbers_scanned = map(int, port_numbers_scanned) # map string representation of port numbers to int to find min and max port number 
print "Part II answer ---  Range of ports at " + portscanned_victim + " scanned by " + portscanned_attacker + " is %d to %d.\n" %(min(port_numbers_scanned),max(port_numbers_scanned))

numTimesFlooded = port_numbers_flood.count("80")
print "Part III answer --- Number of SYN packets " + portflood_attacker +  " sent to port 80 on address " + portflood_victim + ": %d\n" %numTimesFlooded



# PART IV Find the checksum of the malicious packet injected into the network by my mobile device. 
# Record source and dest IP and port, with sequence number of packet

print "PART IV: Looking for all repeated outgoing TCP transmissions from mobile device... \n\n"
mobile_IP = "10.30.22.101"
index = 0
numFound = 0;
 
transmissions =  [] # list, where tuple is and (sourceIP, destIP, seqno)
repeated_transmissions = [] # second line of repeated transmission entries based on a repeated sequence numbers
repeated_transmissions_indices = [] # line number where the index of the repeated transmission is

for line in dataLines:
	if ( (">" in line) and ("seq" in line) and (not "length 0" in line) ) : # Checks for anything that has " > in it, then it's a transmission"
		secondLine = line # Would be the second line of a well formatted entry. 
		sourceIP_with_port = getSourceIP(secondLine) # With the port number to differentiate UNIQUE TCP session. 
		sourceIP = removePortNumber(sourceIP_with_port) 
		destIP_with_port = getDestIP(secondLine) # With port number to dif
		destIP = removePortNumber(destIP_with_port)

		# if (sourceIP_with_port == "10.30.22.101.64215" and destIP_with_port == "54.246.83.168.443"): print secondLine
		# if (sourceIP_with_port == "54.246.83.168.443" and destIP_with_port == "10.30.22.101.64215"): print secondLine

		if ( sourceIP == mobile_IP): # Check if the mobile IP address is the source IP address, and length is non-zero
				seqno = getseqno(secondLine)
				destIP = getDestIP(secondLine)

				if (transmissions.count( (sourceIP_with_port, destIP_with_port, seqno) ) == 0 ):
					transmissions.append( (sourceIP_with_port, destIP_with_port,seqno) ) # Add to the list of destIP, seqno pairs
				else: 
					repeated_transmissions.append(secondLine) # The current line is a repeated transmission to a destIP of a sequence number
					repeated_transmissions_indices.append(index) # Get index of the entry list of where the repeated transmission was found
					numFound += 1
	index +=1 

i = 0 
for line in repeated_transmissions:
	print "At index #%d the repeated transmission line is: \n:" %repeated_transmissions_indices[i] + line
	i += 1

print "Entries to sort through: %d\n" %numFound

print "The injected packet is below, with checksum value: 0xe1c2. For reference, the previous few lines of the trace.txt file are also shown to demonstrate the non-malicious tranmission and ACK before the injection."
print dataLines[25419]
print dataLines[25420]
print dataLines[25421]
print dataLines[25422]
print repeated_transmissions[0]

"""
The malicious packet injection takes place between lines 25421 to 25423 of the trace.txt file. The server acks with a value of 2062, and then the malicious
device tries to send a packet with sequence number 1663, even though that was already acknowledged. Clearly, there is no proper IP 
header in the injected packet, which is what made parsing annoying...

cksum of malicious packet: 0xe1c2

IP (tos 0x0, ttl 64, id 44874, offset 0, flags [DF], proto TCP (6), length 451)
    10.30.22.101.64154 > 171.67.215.200.80: Flags [P.], cksum 0xc7d4 (correct), seq 1663:2062, ack 186953, win 65535, options [nop,nop,TS val 408566938 ecr 1998633308], length 399
IP (tos 0x0, ttl 250, id 14069, offset 0, flags [DF], proto TCP (6), length 52)
    171.67.215.200.80 > 10.30.22.101.64154: Flags [.], cksum 0x0888 (correct), ack 2062, win 6441, options [nop,nop,TS val 1998633383 ecr 408566938], length 0
    10.30.22.101.64154 > 171.67.215.200.80: Flags [P.], cksum 0xe1c2 (correct), seq 1663:2062, ack 186953, win 65535, options [nop,nop,TS val 408566938 ecr 1998633308], length 399
"""




