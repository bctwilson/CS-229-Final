import numpy as np 
from scipy import stats
import os

a = np.array([1,2,3,4,5])
p = np.percentile(a, 0) # return 50th percentile, e.g median.
print p


scores = [1,2,3,3,4]
print scores
print stats.percentileofscore(np.array(scores), 1, kind = "strict")
print stats.percentileofscore(np.array(scores), 3, kind = "strict")
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.percentileofscore.html #scipy.stats.percentileofscore

#75.0

directory = "/Users/lbwilsonbosque/Dropbox/CS 229/Final Project/SocioDemographic TRACT Level Data"
for filename in os.listdir(directory):
	print filename
	if "EJScreen" not in filename:
		continue 
	print "real file"
		
