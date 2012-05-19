import csv
import re

f = open('flextronics_sample.csv', 'r')
data = f.readlines()
f.close()



print "Found %d lines" %len(data)
print "Found %d ASCII 13 characters" %data[0].count("\x13")
print "Found %d '\\r' characters" %data[0].count("\r")

f = open('flextronics_processed.csv', 'w')
f.write(re.sub("\r", "\n", data[0]))
f.write("\n")
f.close()













