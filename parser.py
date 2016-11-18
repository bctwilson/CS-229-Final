import csv


# Put each line of the file into a python list. 
dataLines = []
print 'Loading file...\n'
numLinesToOpen = 50;
with open('some.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row